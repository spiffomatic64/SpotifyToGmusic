#!/usr/bin/env python3

# This example parses html from a website, to find and print all of the image src urls

# You can install BeautifulSoup using the following command (in console)
#  pip install beautifulsoup4

from bs4 import BeautifulSoup
import requests


def get_uris(url):
    uris = []
    # Get the html from a url
    r  = requests.get(url)
    # The data is stored in a variable called "text" in the returned variable
    data = r.text

    # Let BeautifulSoup parse the data
    soup = BeautifulSoup(data,'html.parser')

    for link in soup.find_all('a', href=True):
        href = link["href"]
        uri_pos = href.find("uri=")
        if uri_pos>0:
            uri = href[uri_pos+4:]
            uris.append(uri)
        
    return uris
    
uris = get_uris("http://everynoise.com/everynoise1d.cgi?scope=mainstream%20only&vector=popularity")
for uri in uris:
    print(uri)
    
'''
<tr valign=top class=>
   <td align=right class=note  style="font-size: 20px; line-height: 24px" >1</td>
   <td  style="font-size: 20px; line-height: 24px"> <a href="https://embed.spotify.com/?uri=spotify:user:thesoundsofspotify:playlist:6gS3HhOiI17QNojjPuPzqc" class=note target=spotify title="See this playlist" onclick="linksync('https://embed.spotify.com/?uri=spotify:user:thesoundsofspotify:playlist:6gS3HhOiI17QNojjPuPzqc');">&#x260A;</a></td>
   <td class=note  style="font-size: 20px; line-height: 24px"><a href="?root=pop&scope=mainstream only" title="Re-sort the list starting from here."  style="color: #B18610">pop</a></td>
</tr>
'''
