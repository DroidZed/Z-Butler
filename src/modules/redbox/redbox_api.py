import redis


def main():

    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.set("bot", "z-butler")
    print(r.get("bot"))


if __name__ == "__main__":
    main()
