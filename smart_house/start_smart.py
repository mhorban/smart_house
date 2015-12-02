from oslo_config import cfg 
from oslo_log import log as logging

CONF = cfg.CONF
#CONF.import_opt('enabled_apis', 'nova.service')

# import DB options
# import sensor's server options

def main():
    config.parse_args(sys.argv)                                        
    logging.setup(CONF, "smart") 
    
    # connect to db
    
    # apply all rules
    
    # optionally start listen 'active' sensors
