# Analyzing shard data
## Question:
You have an elasticsearch cluster, whose state you need to analyze.
Your script will be given the output of /_cat/shards api from elasticsearch.
The api outputs a table of all the shards in your elasticsearch cluster.
> Sample input
```
zeta 0 p STARTED    3014 31.1mb 192.168.56.10 H5dfFeA
zeta 0 r UNASSIGNED
meta 1 r STARTED    3014 31.1gb 192.168.56.20 I8hydUG
```
Columns are in this sequence: (index-name) (shard number) (primary ‘p’ or replica ‘r’) (state) (document count) (store size) (node IP) (node name)
Possible states of the shard: STARTED, UNASSIGNED

Write a script which will read the above api outputs from a file, and analyze the cluster. Your script needs to output: 
- Number of primary shards and replica shards, separately.
- Total size occupied by the primary shards and replica shards, separately. Use mb, gb, kb etc. measurement unit depending on the magnitude (size magnitude must be > 0). For example, if the total storage is 0.5gb, mention it as 500.0mb to improve readability. Similarly, to represent 19824.0 mb, you'll use 19.4 gb. Output upto one decimal place, the smallest shard size unit is kb, largest is tb.
- Name of the elasticsearch node where the disk usage is maximum out of all nodes.
- Assume a 128gb disk for each node; list the nodes where the 80% disk watermark has been crossed.
> Sample output:
```
count: [primary: 7, replica: 15]
size: [primary: 718.0mb, replica: 1.3gb]
disk-max-node: H5dfFeA
watermark-breached: [H5dfFeA, I8hydUG]
```

# Run:
```
cat input/sample-input | python app.py
```