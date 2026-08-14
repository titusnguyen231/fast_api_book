import importlib,traceback,sys
try:
    m = importlib.import_module('app.main')
    print('import succeeded')
    print('module file:', getattr(m,'__file__',None))
    keys = sorted([k for k in m.__dict__.keys() if not k.startswith('_')])
    print('keys:', keys)
    print('app exists:', 'app' in m.__dict__)
    print('app value:', repr(m.__dict__.get('app')))
except Exception:
    traceback.print_exc()
    sys.exit(1)
