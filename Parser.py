import ast

import astor

from right_hand_side_visitor import RHSVisitor
from label_visitor import LabelVisitor

# Global Variable that stores the traceable paramaters of fit or fit_gen functions.
traceParams= []

# This class takes tree as input and walks through
# all the nodes are pulls out Import Statements, fit, fit_gen compile functions
class Analyzer(ast.NodeVisitor):

    imports = []
    importFroms = []
    calls = []
    fitParams = []

    nn_end_no = 0
    nn_target_id = ''

    # Parser function that collects all import statements
    def visit_Import(self, node):
        # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        Analyzer.imports.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))

    #  Parser function that collects all import from statements
    def visit_ImportFrom(self, node):
        # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        Analyzer.importFroms.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))


    # Fit Generator, compile functions are collected here
    def visit_Call(self,node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                if value.attr in ["compile"]:
                    Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                if value.attr in ["fit","fit_generator"]:
                    # print('-----------------')
                    # print(value.attr)
                    # print('-----------------')
                    Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                    args = node.args
                    for arg in args:
                        if isinstance(arg, ast.Str):
                            Analyzer.fitParams.append(arg.s)
                        if isinstance(arg, ast.Name):
                            traceParams.append(arg.id)
                            Analyzer.fitParams.append(arg.id)
                    kws = node.keywords
                    for kw in kws:
                        if isinstance(kw.value, ast.Tuple):
                            pars = []
                            for k in kw.value.elts:
                                if isinstance(k, ast.Name):
                                    pars.append(k.id)
                                if isinstance(k, ast.Num):
                                    pars.append(k.n)
                            Analyzer.fitParams.append((kw.arg, pars))
                        if isinstance(kw.value, ast.Num):
                            Analyzer.fitParams.append((kw.arg, kw.value.n))
                        if isinstance(kw.value, ast.Name):
                            traceParams.append(kw.value.id)
                            Analyzer.fitParams.append((kw.arg, kw.value.id))
                        if isinstance(kw.value, ast.List):
                            pars = []
                            for k in kw.value.elts:
                                if isinstance(k, ast.Name):
                                    pars.append(k.id)
                                if isinstance(k, ast.Num):
                                    pars.append(k.n)
                            Analyzer.fitParams.append((kw.arg, pars))
                if value.attr in ["compile"]:
                    Analyzer.nn_end_no = value.lineno
                    Analyzer.nn_target_id = value.value.id


#This class takes the tree as input and
# traces back the variables of fit functions
class Tracker(ast.NodeVisitor):
    paramsStatements = []
    def visit_Assign(self, node):
        rhs_visitor = RHSVisitor()
        rhs_visitor.visit(node.value)
        if isinstance(node.targets[0], ast.Tuple):  # x,y = [1,2]
            if isinstance(node.value, ast.Tuple):
                for i, target in enumerate(node.targets[0].elts):
                    if isinstance(target, ast.Name) &  (target.id in traceParams):
                        value = node.value.elts[i]
                        label = LabelVisitor()
                        label.visit(target)
                        if isinstance(value, ast.Call):
                            Tracker.paramsStatements.append(label.result)
                        else:
                            label.result += ' = '
                            label.visit(value)
                            Tracker.paramsStatements.append(label.result)

            elif isinstance(node.value, ast.Call):
                call = None
                for element in node.targets[0].elts:
                    if element in traceParams:
                        label = LabelVisitor()
                        label.visit(element)
                        left_hand_label = label.result
                        label = LabelVisitor()
                        label.visit(node.value)
                        Tracker.paramsStatements.append(left_hand_label + '=' + label.result)

        elif len(node.targets) > 1:  # x = y = 3
            for target in node.targets:
                label = LabelVisitor()
                label.visit(target)
                if label.result in traceParams:
                    label.result += ' = '
                    label.visit(node.value)
                    Tracker.paramsStatements.append(label.result)

        else:
            label = LabelVisitor()
            label.visit(node.targets[0])
            left_hand_label = label.result
            if left_hand_label in traceParams:
                if isinstance(node.value, ast.Call):  # x = call()
                    label = LabelVisitor()
                    label.visit(node.value)
                    Tracker.paramsStatements.append(left_hand_label + '=' + label.result)

                else:  # x = 4
                    label = LabelVisitor()
                    label.visit(node)
                    Tracker.paramsStatements.append(label.result)

class Node(object):
    """A Control Flow Graph node that contains a list of ingoing and outgoing nodes and a list of its variables."""

    def __init__(self, label, ast_node, *, line_number, path):
        """Create a Node that can be used in a CFG.
        Args:
            label (str): The label of the node, describing the expression it represents.
            line_number(Optional[int]): The line of the expression the Node represents.
        """
        self.ingoing = list()
        self.outgoing = list()

        self.label = label
        self.ast_node = ast_node
        self.line_number = line_number
        self.path = path

        # Used by the Fixedpoint algorithm
        self.old_constraint = set()
        self.new_constraint = set()

    def connect(self, successor):
        """Connect this node to its successor node by setting its outgoing and the successors ingoing."""
        if isinstance(self, ConnectToExitNode) and not type(successor) is EntryExitNode:
            return
        self.outgoing.append(successor)
        successor.ingoing.append(self)

    def connect_predecessors(self, predecessors):
        """Connect all nodes in predecessors to this node."""
        for n in predecessors:
            self.ingoing.append(n)
            n.outgoing.append(self)

    def __str__(self):
        """Print the label of the node."""
        return ' '.join(('Label: ', self.label))

    def __repr__(self):
        """Print a representation of the node."""
        label = ' '.join(('Label: ', self.label))
        line_number = 'Line number: ' + str(self.line_number)
        outgoing = ''
        ingoing = ''
        if self.ingoing is not None:
            ingoing = ' '.join(('ingoing:\t', str([x.label for x in self.ingoing])))
        else:
            ingoing = ' '.join(('ingoing:\t', '[]'))

        if self.outgoing is not None:
            outgoing = ' '.join(('outgoing:\t', str([x.label for x in self.outgoing])))
        else:
            outgoing = ' '.join(('outgoing:\t', '[]'))

        if self.old_constraint is not None:
            old_constraint = 'Old constraint:\t ' + ', '.join([x.label for x in self.old_constraint])
        else:
            old_constraint = 'Old constraint:\t '

        if self.new_constraint is not None:
            new_constraint = 'New constraint: ' + ', '.join([x.label for x in self.new_constraint])
        else:
            new_constraint = 'New constraint:'
        return '\n' + '\n'.join((label, line_number, ingoing, outgoing, old_constraint, new_constraint))


class ConnectToExitNode():
    pass

class EntryExitNode(Node):
    """CFG Node that represents a Exit or an Entry node."""

    def __init__(self, label):
        super(EntryExitNode, self).__init__(label, None, line_number=None, path=None)

class AssignmentNode(Node):
    """CFG Node that represents an assignment."""

    def __init__(self, label, left_hand_side, ast_node, right_hand_side_variables, *, line_number, path):
        """Create an Assignment node.
        Args:
            label (str): The label of the node, describing the expression it represents.
            left_hand_side(str): The variable on the left hand side of the assignment. Used for analysis.
            right_hand_side_variables(list[str]): A list of variables on the right hand side.
            line_number(Optional[int]): The line of the expression the Node represents.
        """
        super(AssignmentNode, self).__init__(label, ast_node, line_number=line_number, path=path)
        self.left_hand_side = left_hand_side
        self.right_hand_side_variables = right_hand_side_variables

    def __repr__(self):
        output_string = super(AssignmentNode, self).__repr__()
        output_string += '\n'
        return ''.join((output_string, 'left_hand_side:\t', str(self.left_hand_side), '\n',
                        'right_hand_side_variables:\t', str(self.right_hand_side_variables)))


# Neural Network Schema Analyser
class GlobalUseCollector(ast.NodeVisitor):
    occurances = []
    def __init__(self, name):
        self.name = name
        # track context name and set of names marked as `global`
        self.context = [('global', ())]

    def visit_FunctionDef(self, node):
        self.context.append(('function', set()))
        self.generic_visit(node)
        self.context.pop()

    def visit_ClassDef(self, node):
        self.context.append(('class', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Lambda(self, node):
        # lambdas are just functions, albeit with no statements
        self.context.append(('function', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Global(self, node):
        assert self.context[-1][0] == 'function'
        self.context[-1][1].update(node.names)

    def visit_Name(self, node):
        ctx, g = self.context[-1]
        if node.id == self.name and (ctx == 'global' or node.id in g):
            # print('{} used at line {}'.format(node.id, node.lineno))
            GlobalUseCollector.occurances.append(node.lineno)


# Neural Network Extracter
class NNExtracter(ast.NodeVisitor):

    cnnStatements = []

    def visit_Assign(self, node):
        if node.lineno in GlobalUseCollector.occurances and node.lineno < Analyzer.nn_end_no:
            NNExtracter.cnnStatements.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))

    def visit_Call(self,node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                if value.lineno in GlobalUseCollector.occurances and value.lineno < Analyzer.nn_end_no:
                    NNExtracter.cnnStatements.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))


class AST:
    # Iterator utility function. It has 3 params
    # list to be written to file - ls
    # message to be shown on the top of the file
    # filename- filename to be created in the output
    def iterator(ls, message, filename):
        file = open('./output/' + filename, 'a');
        file.write("\n\n" + message + ": \n")
        file.write("-------------------------- \n")
        for ob in ls:

            file.write(str(ob) + "\n")

        file.close()

    # main function
    def ParseAst(self, path):
        tree = astor.code_to_ast.parse_file(path)
        analyzer = Analyzer()
        analyzer.visit(tree)

        tracker = Tracker()
        tracker.visit(tree)

        GlobalUseCollector(Analyzer.nn_target_id).visit(tree)
        NNExtracter().visit(tree)

        hyperparamas = tracker.paramsStatements
        return hyperparamas

