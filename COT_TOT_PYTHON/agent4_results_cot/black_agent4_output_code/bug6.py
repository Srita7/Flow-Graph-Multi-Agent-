def buggy_function(rs, data, freq=None):
    TargetVersion.PY27: set(),
        TargetVersion.PY33: {Feature.UNICODE_LITERALS},
        TargetVersion.PY34: {Feature.UNICODE_LITERALS},
        TargetVersion.PY35: {Feature.UNICODE_LITERALS, Feature.TRAILING_COMMA_IN_CALL},
    def get_grammars(target_versions: Set[TargetVersion]) -> List[Grammar]:
                pygram.python_grammar_no_print_statement_no_exec_statement,
                pygram.python_grammar_no_print_statement,
                pygram.python_grammar,
            return [pygram.python_grammar_no_print_statement, pygram.python_grammar]
            return [pygram.python_grammar_no_print_statement_no_exec_statement]
        for grammar in get_grammars(set(target_versions)):
            drv = driver.Driver(grammar, pytree.convert)
        def __init__(self, grammar, convert=None, logger=None):
            tokens = tokenize.generate_tokens(stream.readline)
            tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        def generate_tokens(readline):
            async_def = False # Added for b5->b6
            if