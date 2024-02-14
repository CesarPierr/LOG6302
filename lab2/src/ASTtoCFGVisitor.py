# This is an example of a visitor to create a CFG
# You can start from here


from code_analysis import ASTException, CFG, AST


class ASTtoCFGVisitor:
    def __init__(self):
        self.ast = None
        self.cfg = CFG()
        self.iNextNode = 0

    def get_new_node(self) -> int:
        self.iNextNode += 1
        return self.iNextNode

    def visit(self, ast: AST):
        self.iNextNode = 0
        self.ast = ast
        self.cfg = CFG()
        print(f"Visit AST from file {self.ast.get_filename()}")
        self.visit_ROOT()
        return self.cfg

    def visit_ROOT(self):
        ctx = {}
        entryNodeId = self.get_new_node()
        stopNodeId = self.get_new_node()
        rootAST = self.ast.get_root()
        self.cfg.set_root(entryNodeId)

        self.cfg.set_type(entryNodeId, "Entry")
        self.cfg.set_image(entryNodeId, "main")
        self.cfg.set_type(stopNodeId, "Exit")

        ctx['parent'] = entryNodeId
        ctx['scope'] = entryNodeId
        ctx['stopId'] = stopNodeId

        if self.ast.get_type(rootAST) == "Start":
            self.cfg.set_node_ptr(rootAST, entryNodeId)

        self.visit_node(rootAST, ctx)
        self.cfg.add_edge(ctx['endId'], stopNodeId)

    # chain nodes
    def visit_GENERIC(self, ast_node_id: int, ctx: dict) -> int:
        cfg_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, cfg_node)
        self.cfg.set_type(cfg_node, self.ast.get_type(ast_node_id))
        self.cfg.set_image(cfg_node, self.ast.get_image(ast_node_id))
        if ctx["parent"] is not None:
            self.cfg.add_edge(ctx["parent"], cfg_node)

        ctx["endId"] = cfg_node

        new_ctx = dict(ctx) # clone ctx
        new_ctx["parent"] = cfg_node
        for child_id in self.ast.get_children(ast_node_id):
            self.visit_node(child_id, new_ctx)
            new_ctx["parent"] = new_ctx["endId"]
        ctx["endId"] = new_ctx["endId"]

        return cfg_node

    def visit_GENERIC_BLOCK(self, ast_node_id: int, ctx: dict):
        new_ctx = dict(ctx) # clone ctx
        for child_id in self.ast.get_children(ast_node_id):
            self.visit_node(child_id, new_ctx)
            new_ctx["parent"] = new_ctx["endId"]
        ctx["endId"] = new_ctx["endId"]

        return None

    def visit_BINOP(self, ast_node_id: int, ctx: dict) -> int:
        #Create BinOP node
        binOp_type = self.ast.get_type(ast_node_id)
        cfg_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, cfg_node)
        self.cfg.set_type(cfg_node, self.ast.get_type(ast_node_id))
        self.cfg.set_image(cfg_node, self.ast.get_image(ast_node_id))

        begin = 0
        if binOp_type == "BinOP":
            begin = 1
        #Visit right child
        new_ctx = dict(ctx) # clone ctx
        self.visit_node(self.ast.get_children(ast_node_id)[begin], new_ctx)
        right = new_ctx['endId']

        #Visit right left
        new_ctx = dict(ctx) # clone ctx
        new_ctx["parent"] = right
        self.visit_node(self.ast.get_children(ast_node_id)[(begin+1)%2], new_ctx)
        left = new_ctx['endId']

        #Link left child with BinOp
        self.cfg.add_edge(left, cfg_node)

        #add coloured arrows 
        if binOp_type == "BinOP":
            self.cfg.set_op_hands(cfg_node,left, right)
        elif binOp_type == "RelOP":
            self.cfg.set_op_hands(cfg_node,left, right)          

        ctx["endId"] = cfg_node
        return cfg_node

    def continue_or_break(self, ast_node_id: int, ctx: dict) -> int:
        cur_type = self.ast.get_type(ast_node_id)
        node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, node)
        self.cfg.set_type(node, cur_type)
        self.cfg.add_edge(ctx["endId"], node)
        
        begin = ctx["scope"]
        end = begin +1
        ctx["endId"] = None
        if cur_type == "Continue":
            self.cfg.add_edge(node, begin)
        elif cur_type == "Break":
            self.cfg.add_edge(node, end)
        
        
    def visit_if_then_else(self, ast_node_id: int, ctx: dict) -> int:
        #Create If and Ifend nodes
        
        if_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, if_node)
        self.cfg.set_type(if_node, 'If')
        self.cfg.add_edge(ctx["parent"], if_node)
        
        
        endif_node = self.get_new_node()
        self.cfg.set_type(endif_node, 'IfEnd')        
        
        #treat condition (left child)
        new_ctx = dict(ctx)
        new_ctx["parent"] = if_node 
        self.visit_node(self.ast.get_children(ast_node_id)[0], new_ctx)
        end_op = new_ctx['endId']
        
        #treat then the two conditions middle and right child
        new_ctx = dict(ctx)
        new_ctx["parent"] = end_op
        self.visit_node(self.ast.get_children(ast_node_id)[1], new_ctx)
        self.cfg.add_edge(new_ctx['endId'], endif_node)
        

        #treat else 
        new_ctx = dict(ctx)
        new_ctx["parent"] = end_op
        self.visit_node(self.ast.get_children(ast_node_id)[2], new_ctx)
        self.cfg.add_edge(new_ctx['endId'], endif_node)
            
        ctx["endId"] = endif_node
        return endif_node
    
    def visit_IfThen(self, ast_node_id: int, ctx: dict) -> int:
        
        if_node = self.get_new_node()
        self.cfg.add_edge(ctx["endId"], if_node)
        self.cfg.set_type(if_node, 'If')
        ctx["parent"] = if_node
        
        endif_node = self.get_new_node()
        self.cfg.set_type(endif_node, 'IfEnd')
        
        #visit condition
        new_ctx = dict(ctx)
        self.visit_node(self.ast.get_children(ast_node_id)[0], new_ctx)

        end_id = new_ctx['endId']
        
        self.visit_node(self.ast.get_children(ast_node_id)[1], new_ctx)

        #link endid with endif_node
        self.cfg.add_edge(end_id, endif_node)
        
        ctx["endId"] = endif_node
        return endif_node
    
    def visit_Condition(self, ast_node_id: int, ctx: dict) -> int:
        
        #visit its first child
        new_ctx = dict(ctx)
        self.visit_node(self.ast.get_children(ast_node_id)[0], new_ctx)
        
        condition_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, condition_node)
        self.cfg.set_type(condition_node, 'Condition')
        
        #link the condition node with the ctx parent
        self.cfg.add_edge(new_ctx['endId'], condition_node)
        
        ctx["endId"] = condition_node
        
        return condition_node
        
    def visit_ArgumentList(self, ast_node_id: int, ctx: dict) -> int:
        
        #create ArgumentList node
        argumentList_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, argumentList_node)
        self.cfg.set_type(argumentList_node, 'ArgumentList')
        self.cfg.add_edge(ctx["parent"], argumentList_node)        
        ctx["parent"] = argumentList_node
        
        self.visit_node(self.ast.get_children(ast_node_id)[0], ctx)
        end_id = ctx['endId']
        
        #create argument node
        argument_node = self.get_new_node()
        self.cfg.set_type(argument_node, 'Argument')
        self.cfg.add_edge(end_id, argument_node)
        ctx["endId"] = argument_node
        
        
        return argument_node
        
        
    def visit_While(self, ast_node_id: int, ctx: dict) -> int:
        #Create While and WhileEnd nodes
        while_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, while_node)
        self.cfg.set_type(while_node, 'While')
        self.cfg.add_edge(ctx["parent"], while_node)
        
        whileend_node = self.get_new_node()
        self.cfg.set_type(whileend_node, 'WhileEnd')
        
        #treat condition (left child)
        new_ctx = dict(ctx)
        new_ctx["parent"] = while_node 
        new_ctx["scope"] = while_node
        self.visit_node(self.ast.get_children(ast_node_id)[0], new_ctx)
        end_op = new_ctx['endId']
        
        #set parent of whileend node
        self.cfg.add_edge(new_ctx['endId'], whileend_node)
        
                
        new_ctx["parent"] = end_op
        self.visit_node(self.ast.get_children(ast_node_id)[1], new_ctx)
        self.cfg.add_edge(new_ctx['endId'], while_node)
        
        ctx["endId"] = whileend_node
        
        
        return whileend_node
    
    def visit_function(self, ast_node_id: int, ctx: dict) -> int:
        
        #get left child id function
        function_node = self.get_new_node()
        self.cfg.set_node_ptr(ast_node_id, function_node)
        self.cfg.set_type(function_node, 'FunctionCall')
        self.cfg.add_edge(ctx["parent"], function_node)
        
        callbegin_node = self.get_new_node()
        self.cfg.set_type(callbegin_node, 'CallBegin')
        callend_node = self.get_new_node()
        self.cfg.set_type(callend_node, 'CallEnd')
        #get right child id argumentList
        new_ctx = dict(ctx)
        new_ctx["parent"] = function_node
        self.visit_node(self.ast.get_children(ast_node_id)[0], new_ctx)
        new_ctx["parent"] = new_ctx["endId"]
        image = self.cfg.get_image(new_ctx["endId"])
        id_node_id = new_ctx["endId"]
        
        self.visit_node(self.ast.get_children(ast_node_id)[1], new_ctx)
        
        args_id = new_ctx["endId"]
        #generate CallBegin and CallEnd nodes (call end is the end and direct child of call begin)
        self.cfg.set_image(callbegin_node, image)
        self.cfg.add_edge(new_ctx["endId"], callbegin_node)
        
        self.cfg.set_image(callend_node, image)
        self.cfg.add_edge(callbegin_node, callend_node)
        self.cfg.set_op_hands(callbegin_node,id_node_id, args_id-1)
        
        #add node RetValue
        ret_value_node = self.get_new_node()
        self.cfg.set_type(ret_value_node, 'RetValue')
        self.cfg.add_edge(callend_node, ret_value_node)
        
        ctx["endId"] = ret_value_node        
        return callend_node        
    
        
        
    def visit_node(self, ast_node_id: int, ctx: dict):
        cur_type = self.ast.get_type(ast_node_id)
        if cur_type is None:
            raise ASTException("Missing type in a node")

        if cur_type in ["BinOP", "RelOP", "LogicOP"]:
            self.visit_BINOP(ast_node_id, ctx)
        elif cur_type in ["IfThenElseStatement"]:
            self.visit_if_then_else(ast_node_id, ctx)
        elif cur_type in ["IfThenStatement"]:
            self.visit_IfThen(ast_node_id, ctx)
        elif cur_type in ["ArgumentList"]:
            self.visit_ArgumentList(ast_node_id, ctx)
        elif cur_type in ["Condition"]:
            self.visit_Condition(ast_node_id, ctx)
        elif cur_type in ["Continue", "Break"]:
            self.continue_or_break(ast_node_id, ctx)
        elif cur_type in ["While"]:
            self.visit_While(ast_node_id, ctx)
        elif cur_type in ["FunctionCall"]:
            self.visit_function(ast_node_id, ctx)
        elif cur_type in ["Block", "Start"]:
            self.visit_GENERIC_BLOCK(ast_node_id, ctx)
        elif cur_type in ["PLACEHOLDER", "StatementBody"]: # Node to ignore
            self.visit_passthrough(ast_node_id, ctx)
        else:
            self.visit_GENERIC(ast_node_id, ctx)

    def visit_passthrough(self, ast_node_id: int, ctx: dict):
        for child_id in self.ast.get_children(ast_node_id):
            self.visit_node(child_id, ctx)

