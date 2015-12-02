import sys

from oslo_config import cfg
from oslo_log import log as logging

from smart_house import sql_model

CONF = cfg.CONF

opts = [
    cfg.StrOpt('logger_name',
               default="smart_log",
               help='Name of the logger.'),
    ]

CONF.register_opts(opts)


def parse_args(argv, default_config_files=None):
    logging.register_options(CONF)
    CONF(argv[1:],
         project='smart',
         version='smart 0.0.1',
         default_config_files=default_config_files)


def main():
    parse_args(sys.argv)
    logging.setup(CONF, CONF.logger_name)
    log = logging.getLogger(__name__)
    log.info('Starting Smart')

    sql_model.connect_db()

    # apply all rules

    # optionally start listen 'active' sensors


if __name__ == "__main__":
    main()
