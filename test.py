import requests
import json
from datetime import datetime



ELASTIC_URL = 'https://10.1.1.221:9200/packetbeat-*/_search?size=0'
HEADERS = {'Content-Type': 'application/json'}
AUTH = ('elastic', 'yourstrongpasswordhere')
QUERY_DATA = {
    "query": {
        "range": {
            "@timestamp": {
                "gte": "now-5m",
                "lte": "now"
            }
        }
    },
    "aggs": {
        "tlds": {
            "terms": {
                "field": "dns.question.etld_plus_one",
                "size": 10
            },
            "aggs": {
                "unique_domains": {
                    "cardinality": {
                        "field": "dns.question.name"
                    }
                }
            }
        }
    }
}

start_time = datetime(2023, 9, 1, 10, 6, 0)
end_time = datetime(2023, 9, 1, 10, 30, 0)

query1 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"dns.question.etld_plus_one": "president.gov.by"}},
                {"range": {"@timestamp": {"gte": "2023-09-01 10:06:00", "lte": end_time.isoformat()}}}
            ]
        }
    }
}


def get_request(query: dict) -> dict:
    response = requests.post(ELASTIC_URL, headers=HEADERS, auth=AUTH, json=query, verify=False)
    return json.loads(response.content.decode("utf-8"))


def write_to_file(domain_name: str) -> None:
    with open("ddos_domain_by_zone.txt", "a") as file:
        file.write(f"{domain_name}, timestamp: {datetime.now()}")


def main():
    data = get_request(query1)
    print(len(data))
    #t = 0
    #for k, v in data.items():
    #    print(k, v)
    #    if t == 20:
    #        break
    print("================================IT'S ALL==========================================")


if __name__ == "__main__":
    main()
