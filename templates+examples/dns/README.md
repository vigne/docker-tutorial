# Basic DNS Example

## Idea

Start two Alpine container and keep them running using *tail -f /dev/null*
Then use docker exec to ping each other.

## Usage

	[ralph@donald dns_example]$ docker-compose up -d

	[ralph@donald dns_example]$ docker exec -it hostB ping hostA
	PING hostA (172.22.0.3): 56 data bytes
	64 bytes from 172.22.0.3: seq=0 ttl=64 time=0.111 ms
	64 bytes from 172.22.0.3: seq=1 ttl=64 time=0.253 ms
	64 bytes from 172.22.0.3: seq=2 ttl=64 time=0.267 ms
	^C
	--- hostA ping statistics ---
	3 packets transmitted, 3 packets received, 0% packet loss
	round-trip min/avg/max = 0.111/0.210/0.267 ms



	[ralph@donald dns_example]$ docker exec -it hostA ping hostB
	PING hostB (172.22.0.2): 56 data bytes
	64 bytes from 172.22.0.2: seq=0 ttl=64 time=0.069 ms
	64 bytes from 172.22.0.2: seq=1 ttl=64 time=0.327 ms
	64 bytes from 172.22.0.2: seq=2 ttl=64 time=0.253 ms
	^C
	--- hostB ping statistics ---
	3 packets transmitted, 3 packets received, 0% packet loss
	round-trip min/avg/max = 0.111/0.210/0.267 ms


