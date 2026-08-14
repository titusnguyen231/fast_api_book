import runpy
g = runpy.run_path('d:/fast_api_book/app/main.py')
print('run_path keys:', sorted([k for k in g.keys() if not k.startswith('_')]))
print('app in g?', 'app' in g)
print('app value:', g.get('app'))
