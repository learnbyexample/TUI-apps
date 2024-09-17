def greeting(ip, style='-', spacing=6, char=' '):
    op_length = spacing + len(ip)
    styled_line = (style * op_length)[:op_length]
    print(styled_line)
    print(f'{ip:{char}^{op_length}}')
    print(styled_line)

greeting('hi')
greeting('hello', style='*', char='/')
greeting('good day', spacing=20)
greeting('pomegranate', style='=-=')
greeting('fig', ':', 2, '=')
