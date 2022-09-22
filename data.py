from bs4 import BeautifulSoup as bs



def get_info(handle, website):	def get_info(handle, website):
    website = website.lower()	    website = website.lower()
    if website == 'codechef':	    if website == 'codechef':
@@ -18,9 +19,12 @@ def get_info(handle, website):
        return get_yuki(handle)	        return get_yuki(handle)
    elif website == 'uri':	    elif website == 'uri':
        return get_uri(handle)	        return get_uri(handle)
    elif website == 'leetcode':
        return get_leetcode(handle)
    else:	    else:
        raise ValueError('wrong platform website name')	        raise ValueError('wrong platform website name')



def get_cf(user):	def get_cf(user):
    r = requests.get(f"https://codeforces.com/profile/{user}").text	    r = requests.get(f"https://codeforces.com/profile/{user}").text
    soup = bs(r, 'lxml')	    soup = bs(r, 'lxml')
@@ -128,20 +132,39 @@ def get_yuki(user):
    color = '#2ecc71'	    color = '#2ecc71'
    return [level, color]	    return [level, color]



def get_uri(user_id):	def get_uri(user_id):
	url = f'https://www.urionlinejudge.com.br/judge/pt/profile/{user_id}'	    url = f'https://www.urionlinejudge.com.br/judge/pt/profile/{user_id}'
	r = requests.get(url).text	    r = requests.get(url).text


	soup = bs(r, 'html.parser')	    soup = bs(r, 'html.parser')
	s = soup.find('ul', class_='pb-information')	    s = soup.find('ul', class_='pb-information')
	s = [word.lower() for word in s.text.split()]	    s = [word.lower() for word in s.text.split()]


	points = 0	    points = 0
	if 'pontos:' in s:	    if 'pontos:' in s:
		strpoints = s[s.index('pontos:')+1].replace('.', '')	        strpoints = s[s.index('pontos:')+1].replace('.', '')
		points = int(strpoints[:strpoints.index(',')])	        points = int(strpoints[:strpoints.index(',')])
	elif 'points:' in s:	    elif 'points:' in s:
		strpoints = s[s.index('points:')+1].replace('.', '')	        strpoints = s[s.index('points:')+1].replace('.', '')
		points = int(strpoints[:strpoints.index(',')])	        points = int(strpoints[:strpoints.index(',')])


	return [points, '#F9A908']	    return [points, '#F9A908']


def get_leetcode(username):
    url = 'http://leetcode.com/graphql'
    queryString = '''query getContestRankingData($username: String!) {
                        userContestRankingHistory(username: $username) {
                                rating
                            }
                    }'''
    variables = {
        "username": username,
    }
    r = requests.get(url, json={'query': queryString, 'variables': variables})
    json_data = r.json()
    rankings = max([d['rating']
                    for d in json_data['data']['userContestRankingHistory']])
    rankings = int(rankings)
    return [rankings, '#FFA116']
  20  
main.py
@@ -12,7 +12,8 @@
    'atcoder': 'https://img.atcoder.jp/assets/atcoder.png',	    'atcoder': 'https://img.atcoder.jp/assets/atcoder.png',
    'topcoder': 'https://raw.githubusercontent.com/donnemartin/interactive-coding-challenges/master/images/logo_topcoder.png',	    'topcoder': 'https://raw.githubusercontent.com/donnemartin/interactive-coding-challenges/master/images/logo_topcoder.png',
    'yukicoder': 'https://pbs.twimg.com/profile_images/875757061669232640/T1_mPQuO_400x400.jpg',	    'yukicoder': 'https://pbs.twimg.com/profile_images/875757061669232640/T1_mPQuO_400x400.jpg',
    'uri': 'https://www.urionlinejudge.com.br/judge/img/5.0/logo.130615.png?1591503281'	    'uri': 'https://www.urionlinejudge.com.br/judge/img/5.0/logo.130615.png?1591503281',
    'leetcode': 'https://raw.githubusercontent.com/LeetCode-OpenSource/vscode-leetcode/master/resources/LeetCode.png',
}	}


website_text = {	website_text = {
@@ -21,7 +22,8 @@
    'codeforces': 'Codeforces',	    'codeforces': 'Codeforces',
    'topcoder': 'TopCoder',	    'topcoder': 'TopCoder',
    'yukicoder': 'YukiCoder',	    'yukicoder': 'YukiCoder',
    'uri': 'URI'	    'uri': 'URI',
    'leetcode': 'LeetCode',
}	}




@@ -35,17 +37,21 @@ def get_badge(handle, website):
    x = get_info(handle, website)	    x = get_info(handle, website)
    rating, color = str(x[0]), str(x[1])	    rating, color = str(x[0]), str(x[1])
    text = website_text[website.lower()]	    text = website_text[website.lower()]
    	
    if display_logo:	    if display_logo:
        if display_link:	        if display_link:
            badge = pybadges.badge(left_text=text, right_text=rating, right_color=color, logo=logo, embed_logo=True, left_link=link)	            badge = pybadges.badge(left_text=text, right_text=rating,
                                   right_color=color, logo=logo, embed_logo=True, left_link=link)
        else:	        else:
            badge = pybadges.badge(left_text=text, right_text=rating, right_color=color, logo=logo, embed_logo=True)	            badge = pybadges.badge(
                left_text=text, right_text=rating, right_color=color, logo=logo, embed_logo=True)
    else:	    else:
        if display_link:	        if display_link:
            badge = pybadges.badge(left_text=text, right_text=rating, right_color=color, left_link=link)	            badge = pybadges.badge(
                left_text=text, right_text=rating, right_color=color, left_link=link)
        else:	        else:
            badge = pybadges.badge(left_text=text, right_text=rating, right_color=color)	            badge = pybadges.badge(
                left_text=text, right_text=rating, right_color=color)
    response = flask.make_response(badge)	    response = flask.make_response(badge)
    response.content_type = 'image/svg+xml'	    response.content_type = 'image/svg+xml'
    return response	    return response
