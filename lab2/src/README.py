
from code_analysis import CFGReader
reader = CFGReader()
cfg = reader.read_cfg("../part_2/code_mort/example1.php.cfg.json")
cfg.show(filename="example1.cfg.dot")

