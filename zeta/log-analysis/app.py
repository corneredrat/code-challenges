import sys
"""
1)  Number of primary shards and replica shards, separately.
2)  Total size occupied by the primary shards and replica shards, separately. Use mb, gb, kb etc. measurement unit depending on the magnitude (size magnitude must be > 0). For example, if the total storage is 0.5gb, mention it as 500.0mb to improve readability. Similarly, to represent 19824.0 mb, you'll use 19.4 gb. Output upto one decimal place, the smallest shard size unit is kb, largest is tb.
3)  Name of the elasticsearch node where the disk usage is maximum out of all nodes.
4)  Assume a 128gb disk for each node; list the nodes where the 80% disk watermark has been crossed.

"""
# Req 1
primary_shards          = 0
secondary_shards        = 0
# Req 2
total_size_primary      = 0
total_size_secondary    = 0
# Req 3
max_size_node_name      = ""
# Req 4
watermark_breached      = []
log_elements            = []

class log_element:
    """Class that represent elements of a line in the log
    """
    index_name      = None
    shard_number    = None
    node_type       = None
    state           = None
    document_count  = None
    storage_size    = None
    node_ip         = None
    node_name       = None

    def __init__(self,input):
        """Given a log line as string, puplutate variables of this object
        """
        temp_list = input.split()
        self.index_name     = temp_list[0]
        self.shard_number   = temp_list[1]
        self.node_type      = temp_list[2]
        self.state          = temp_list[3]
        if self.state == "UNASSIGNED":
            self.document_count = 0
            self.storage_size   = 0
            self.node_ip        = ""
            self.node_name      = ""
        else:
            self.document_count = temp_list[4]
            self.storage_size   = self.storage_size_to_kb(temp_list[5])
            self.node_ip        = temp_list[6]
            self.node_name      = temp_list[7]
        
    def storage_size_to_kb(self,storage_size):
        """Convert all the storage sizes into kbs for easy computation
        """
        multiplier  = 1
        val         = float(storage_size[0:-2])
        meter       = storage_size[-2:]
        if "kb" == meter:
            multiplier = 1
        elif "mb" == meter:
            multiplier = 1024
        elif "gb" == meter:
            multiplier = 1024*1024
        return val*multiplier
    
def pretty_print_storage(storage_size):
    """
    Params:
        storage size in kb, float
    Returns:
        printable storage size as string, coverted to mb or gb based on size.
    """
    if storage_size < 1024:
        return str(round(storage_size,1))+"kb"
    elif storage_size/1024 < 1024:
        return str(round(storage_size/1024,1))+"mb"
    elif storage_size/(1024*1024) < 1024:
        return str(round(storage_size/(1024*1024),1))+"gb"
    else :
        return str(round(storage_size/(1024*1024*1024),1))+"tb"
    
def read():
    """ Reads input and populates log_elements array
    Params:
        None
    Returns:
        None
    """
    for line in sys.stdin:
        if line == "\n":
            return
        log_elements.append(log_element(line))

def analyze():
    """ Reads elements in list log_elements, computes and populates global variables accordingly
    Params:
        None
    Returns:
        None
    """
    global secondary_shards
    global total_size_secondary
    global total_size_primary
    global max_size_node_name
    global primary_shards
    max_size = 0
    for log_ele in log_elements:
        print("analyzing node : "+log_ele.node_name)
        print("size ",log_ele.storage_size)
        print("type: ",log_ele.node_type)
        # req 3
        if log_ele.storage_size > max_size:
            max_size_node_name  = log_ele.node_name
            max_size            = log_ele.storage_size
        # req 2 and 1
        if log_ele.node_type == "p":
            primary_shards          = primary_shards+1
            total_size_primary      = total_size_primary+log_ele.storage_size
        elif log_ele.node_type == "r":
            secondary_shards        = secondary_shards+1
            total_size_secondary    = total_size_secondary+log_ele.storage_size
        if log_ele.storage_size > (128*1024*1024)*80/100 :
            watermark_breached.append(log_ele.node_name)

def print_output():
    """Prints ouput of the script, use global variables that was set in analyze stage
    Params:
        None
    Returns:
        None
    """
    print("count: [primary: "+str(primary_shards)+", replica: "+str(secondary_shards)+"]")
    print("size: [primary: "+pretty_print_storage(total_size_primary)+", replica: "+pretty_print_storage(total_size_secondary)+"]")
    print("disk-max-node: "+max_size_node_name)
    print("watermark-breached: "+str(watermark_breached))


if __name__ == "__main__":
    read()
    analyze()
    print_output()   
        
        