logger_level = "DEBUG"

def log_map(level):
        lookup_log_map = {
                "DEBUG"	: 0,
                "INFO"		: 1,
                "ALERT"	: 2,
                "ERROR"	: 3
                }
        return lookup_log_map.get(level, 0)

def log_error(msg, msg_level = "ERROR"):
        curr_weight = log_map(logger_level)
        msg_weight = log_map(msg_level)
        
        if msg_weight >= curr_weight:
	        print(msg)