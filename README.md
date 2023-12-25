# Web-Crawler
---

This Project is one of the project from my Computer Networks class which utilizes sockets to make connections between server and client then collects all the cookies and third-part domains

* Part 1 of this project deals with the connection between client and "tmz.com" by using root DNS servers. 
    - Here's the instruction for the Part 1

    - ## DNS client from scratch

        In this part, you will implement a DNS client to resolve the IP address for tmz.com from scratch using the socket API. You cannot use any libraries/methods that simplify DNS implementation such as `gethostbyname`, `getaddrinfo`, etc.

        You will implement the following:

        - You will first build the DNS request payload from scratch.
        - You will then send the DNS request to a public DNS resolver from this [list](https://www.iana.org/domains/root/servers). If you don’t get a response within 10 seconds, try another resolver from the same region in the list.
        - You will then receive a response from the resolver and unpack it.
        - Upon unpacking the response, you will extract the DNS records and identify the type of DNS record and IP address from each DNS record.
        - Once you get the IP address of tmz.com, you will make an HTTP request to the IP address using the socket API.
        - Measure the RTT between your machine and the public DNS resolver.
        - Measure the RTT between your machine and the tmz.com server (when you make the HTTP request to its IP).

        Note that the [link](https://www.iana.org/domains/root/servers) only contains the list of root DNS servers. You will have to extract the IP of the TLD DNS server and then the authoritative DNS server to get the IP address. You have to use the `sendto()` and `recvfrom()` methods of the [socket API](https://docs.python.org/3/library/socket.html) to send/receive UDP packets. You have to use the `connect()`, `sendall()`, and `recv()` methods for TCP packets. You cannot use any packet construction APIs – we want you to construct the DNS and HTTP requests from scratch.

* Part 2 of this project is the web crawler which reads a csv file with the names of many websites at random then captures the cookies and stores the names of any third party domain. It does this for 1000 websites (This number can be changed for quicker performances).
    - Here's the instruction for the Part 2

    - ## Web crawling and HAR file analysis 

        For this part, you will visit 1,000 different websites and analyze the HTTP traffic while visiting each site. 
        
        You will implement the following:

        - You will automatically crawl the home page of the top 1,000 sites from this [list](top-1m.csv) using Selenium.
        - While visiting each site, you will collect the corresponding HTTP traffic (in HAR files).
            -  Selenium does not download HAR files by default, so you will use it with [browsermobproxy](https://github.com/lightbody/browsermob-proxy) to download HAR files.
            - You will need to include a binary to use browsermobproxy. You can find the binary at this [link](browsermob-proxy).
        - After collecting the HAR files, you will conduct the following analysis:
            - Report the number of requests made to third-party domains when visiting each site. A third-party domain is a domain that does not have the same second-level domain (SLD) as the site you are visiting. For example, when you are visiting google.com, ads.google.com is not a third-party since it has the same second-level domain (google) as google.com. However, doubleclick.net is considered a third-party to google.com. Identify the top-10 most commonly seen third-parties across all sites.
            - Identify the third-party cookies present while visiting each site. Third-party cookies are those cookies that were accessed (set or read) by third-party domains. Identify the top-10 most commonly seen third-party cookies across all sites and describe their intended functionality by referencing [Cookiepedia](https://cookiepedia.co.uk/).



## How to run this code

* ### Part 1
    - Open the terminal in the same directory as 
