import ast
import argparse
import _ast

class nodeVisit(ast.NodeVisitor):
	def visit_Expr(self,node):
		print(ast.dump(node))
		self.generic_visit(node)
	def visit_Assign(self,node):
		print(ast.dump(node))
		self.generic_visit(node)

def main():
	#main function
	parser = argparse.ArgumentParser(description="mutating script")
	parser.add_argument('filename',type=str)
	parser.add_argument('number',type=int)
	args = parser.parse_args()
	f = args.filename
	n = args.number
	source = open(f).read()
	tree = ast.parse(source,filename=f,mode='exec')
	print(ast.dump(tree))
	nodeVisit().visit(tree)
	# test_namespace = {}
	# print(_ast.__file__)
	# for node in tree.body:
	# 	print(node.name)
	# 	wrapper = ast.Module(body=[node])
	# 	try:
	# 		co = compile(wrapper, "<ast>", 'exec')
	# 		exec(co, test_namespace)
	# 	except AssertionError:
	# 		print("Assertion failed on line", node.lineno, ":")
	# 		print(lines[node.lineno])
	# 		if e.args:
	# 			print(e)
	# 		print()
if __name__ == '__main__':
	main()