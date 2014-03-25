## Nebula Toolbelt

### Install:

    pip install nebula

### Usage:

    nebula login
    nebula get <service> <plan> <platform> [<location>]
    nebula status <service_id>
    nebula restart <service_id>
    nebula destroy <service_id>
    nebula list [--all]

    Use Nebula to provision and manipulate various services.

    Supported services:
        PostgreSQL Database

    Supported Platforms:
        Digital Ocean  digital-ocean
        Rackspace      rackspace
        Linode         linode
        AWS            aws

    Choosing Data Centers [<location>]:
        Digital Ocean: NY1, NY2, AM1, AM2, SF1, SP1 (defaults to AM1)
        Rasckspace: DFW, ORD, IAD, SYD, HGK (defaults to Northern Virginia)
        Linode: Not supported yet (defaults to Newark)
        AWS: Not supported yet (defaults to Northern Virginia)

    Options:
      -h --help     Lists help
      -v --verbose  More verbose output of commands
