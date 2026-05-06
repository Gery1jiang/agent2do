
from sandbox import safe_execute

print("测试沙箱执行:")
result = safe_execute('print("Hello, Sandbox!")')
print('stdout:', repr(result['stdout']))
print('stderr:', repr(result['stderr']))
print('error:', result['error'])
