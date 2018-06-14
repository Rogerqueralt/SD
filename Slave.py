from pyactor.context import set_context, create_host, serve_forever, sys

if __name__ == "__main__":
    set_context()
    host_address = 'http://127.0.0.1:%s/' % sys.argv[1]
    host = create_host(host_address)
    registry = host.lookup_url('http://127.0.0.1:1679/registry', 'Registry', 'Master')
    registry.bind(host)

    serve_forever()
