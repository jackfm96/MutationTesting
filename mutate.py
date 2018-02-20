import ast
import _ast
from ast import *
import argparse
import astor
import random

COMPAREPROPORTIONS=1
BINOPPROPORTIONS=1
IGNOREDVALS={"Subscript(value=Attribute(value=Name(id='sys', ctx=Load()), attr='version_info', ctx=Load()), slice=Index(value=Num(n=0)), ctx=Load())"}
IGNOREDVARIABLES=[]
ASSIGNMENTPROPORTIONS=1
"""HELPER FUNCTIONS TAKEN FROM GREEN TREE SNAKES"""

def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)
    
    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

def parseprint(code, filename="<string>", mode="exec", **kwargs):
    """Parse some code from a string and pretty-print it."""
    node = parse(code, mode=mode)   # An ode to the code
    print(dump(node, **kwargs))

""" END OF HELPER FUNCTIONS """

def newOp(c):
    if type(c) == type(_ast.Lt()):
        return _ast.GtE()
    elif type(c) == type(_ast.Gt()):
        return _ast.LtE()
    elif type(c) == type(_ast.GtE()):
        return _ast.Lt()
    elif type(c) == type(_ast.LtE()):
        return _ast.Gt()
    elif type(c) == type(_ast.Eq()):
        return _ast.NotEq()
    elif type(c) == type(_ast.NotEq()):
        return _ast.Eq()
    elif type(c) == type(_ast.Is()):
        return _ast.IsNot()
    elif type(c) == type(_ast.IsNot()):
        return _ast.Is()
    elif type(c) == type(_ast.In()):
        return _ast.NotIn()
    elif type(c) == type(_ast.NotIn()):
        return _ast.In()
    else:
        return c
def newBinOp(o):
    if type(o) == type(_ast.Add()):
        return _ast.Sub()
    elif type(o) == type(_ast.Sub()):
        return _ast.Add()#elif type(o) == type(_ast.)
    elif type(o) == type(_ast.Mult()):
        return _ast.FloorDiv()
    elif type(o) == type(_ast.FloorDiv()):
        return _ast.Mult()
    else:
        return o
class nodeVisit(ast.NodeVisitor):
    """
    Extensions of ast node visit function
    """
    def visit_Expr(self,node):
        #print(ast.dump(node))
        self.generic_visit(node)
    def visit_Assign(self,node):
        #print(ast.dump(node))
        self.generic_visit(node)
    def visit_If(self,node):
        self.generic_visit(node)
    # def visit_Module(self,node):
    #     for child in node.body:
    #         global FUNC_COUNT
    #         FUNC_COUNT+=1
    #         if type(child) == type(_ast.FunctionDef()):
                #parseprint(child)
class nodeTraverser(ast.NodeTransformer):
    # def visit_Name(self, node):
    #     self.generic_visit(node)
    #     if node.id == 'a':
    #         return ast.copy_location(ast.Name(id='c',ctx=ast.Load()), node)
    #     else:
    #         return node
    def visit_FunctionDef(self,node):
        self.generic_visit(node)
        global IGNOREDVARIABLES
        IGNOREDVARIABLES = []
        return node
    def visit_Compare(self,node):
        self.generic_visit(node)
        #print(COMPAREPROPORTIONS)
        a = ast.dump(node.left)
        global IGNOREDVALS
        if  ast.dump(node.left) in IGNOREDVALS:
            return node
        val = random.randrange(0,COMPAREPROPORTIONS)
        if val == 0:
            newO = newOp(node.ops[0])
            node.ops[0] = newO
        return node
    def visit_BinOp(self,node):
        self.generic_visit(node)
        val = random.randrange(0,BINOPPROPORTIONS)
        if val == 0:
            newO = newBinOp(node.op)
            node.op = newO
        return node
    def visit_Assign(self,node):
        #print(ast.dump(node))
        try:
            assigned_var = node.targets[0].id
        except:
            return node
        global IGNOREDVARIABLES
        global ASSIGNMENTPROPORTIONS
        if assigned_var in IGNOREDVARIABLES:
            val = random.randrange(0,ASSIGNMENTPROPORTIONS)
            if val == 0:
                IGNOREDVARIABLES.remove(assigned_var)
                return ast.Pass()
            else:
                return node
        else:
            IGNOREDVARIABLES.append(assigned_var)
            return node
def main():
    parser = argparse.ArgumentParser(description="mutating script")
    parser.add_argument('filename',type=str)
    parser.add_argument('number',type=int)
    args = parser.parse_args()
    f = args.filename
    n = args.number
    # Iterate through given n
    # Remove one out of eight assignments

    # LOWER PROPORTIONS -> MORE CHANGES -> HIGHER TEST SCORE
    # LOOK at downlaoded mutate.py and see what previous proportions are

    global ASSIGNMENTPROPORTIONS
    ASSIGNMENTPROPORTIONS = 3
    for i in range(n):
        # Parse tree
        tree = ast.parse(open(f).read(),filename="./" + f,mode="exec")
        # Traverse tree and store functions
        trash = nodeVisit().visit(tree)
        # Reseed random function
        random.seed((i * 500) + (i * 100) + i + 1200)
        # TODO:  Update Compare proportions
        global COMPAREPROPORTIONS
        COMPAREPROPORTIONS=2+(i // 2)
        global BINOPPROPORTIONS
        BINOPPROPORTIONS=(n//2)-(i//2)+6
        #print(COMPAREPROPORTIONS)
        #print(n)
        # TODO: Use python deepcopy to copy tree in case of failure
        #parseprint(tree)
        tree = nodeTraverser().visit(tree)
        #parseprint(tree)
        #parseprint(tree)
        #print(astor.to_source(tree))
        outfile_name = str(i) + ".py"
        with open(outfile_name,"w") as outfile:
            outfile.write(astor.to_source(tree))
if __name__ == '__main__':
	main()











