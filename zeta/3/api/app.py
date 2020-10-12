from    flask           import Flask, jsonify
from    flask           import Response
import  uuid
import  logging 
import  bisect  
import  redis   
from    redis           import exceptions as r_exceptions

app                 = Flask(__name__)
connection          = None
redis_host          = "localhost"
redis_port          = "6379"
valid_characters    = '`abcdefghijklmnopqrstuvwxyz{'
zset_name           = "words"
api_doc             = "spec.json"

logging.basicConfig(
    format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)

def find_prefix_range(sample):
    """Returns the possible string that appears before given sample, and after it.
    params:
        a sample string
    returns:
        <string, string>
        a string that appears before, a string that appears after - relative to the given sample

    example:
        previous:   raght{
        sample:     raghu
        ...         raghunandan
        ...         raghuu
        next:       raghu{
    refer: https://redislabs.com/ebook/part-2-core-concepts/chapter-6-application-components-in-redis/6-1-autocomplete/6-1-2-address-book-autocomplete/
    """
    posn = bisect.bisect_left(valid_characters, sample[-1:])
    suffix = valid_characters[(posn or 1) - 1]
    return sample[:-1] + suffix + '{', sample + '{'

def add_to_redis(sample):
    """Adds a given work (string) to zset
    Params: 
        sample <string>
    Returns:
        None
    """
    global connection
    try:
        logging.info("updating database")
        connection.zadd(
            zset_name, 
            {
                sample  :0
            }
        )
        logging.info("updated database")
    except Exception as e:
        logging.error(str(e))
        raise("unable to update records")

def get_words(sample):
    """Get words that are matching, and extending the given sample word
    Params:
        sample  <string>
    Returns:
        words   <list>
    """
    # Compute start and end of the temp words that marks the boundary between matching words
    start, end  = find_prefix_range(sample)
    # Inset start and end words that appear at the boundaries of matching words
    connection.zadd(
        zset_name, 
        {
            start   : 0,
            end     : 0
        }
    )
    # Compute inices of the created temp words
    sindex      = connection.zrank(zset_name, start)
    eindex      = connection.zrank(zset_name, end)
    logging.info("index range: "+str(sindex)+"-"+str(eindex))
    # Obtain words between computed boundaries
    words       = connection.zrange(zset_name, sindex+1, eindex-1)
    # Remove temporary words that were created as boundaries
    connection.zrem( zset_name, start)
    connection.zrem( zset_name, end)
    return words


@app.route("/add_word/word=<param>", methods=["POST"])
def add_word(param):
    """ Function that processes add word
    """
    try:
        add_to_redis(param)
        res = Response("updated database")
        res.status_code = 201
        return res
    except Exception as e:
        logging.error(str(e))
        res             = Response("unable to update database: "+str(e))
        res.status_code = 500
        return res

@app.route("/autocomplete/query=<param>", methods=["GET"])
def get_autocomplete(param):
    """ Function that processes get auto-complete suggestion query
    """
    words = get_words(param)
    return str(words)


def connect_to_redis() :
    """ Initialize redis connection
    """
    try:
        global connection
        connection    = redis.Redis(
            host=redis_host,
            port=redis_port,
        )
    except Exception as e:
        logging.error(str(e))
        raise Exception("unable to establish connection")
        return 


if __name__ == '__main__':
    try:
        connect_to_redis()
    except Exception as e:
        logging.error(str(e))
    app.run(host="0.0.0.0")