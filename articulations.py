# ----------------------------------------------------------------------
# Name:     articulations
# Purpose:  Homework 9
#
# Author(s): Kiwibud
#
# ----------------------------------------------------------------------
"""
Enter your docstring with a one-line overview here
and a more detailed description here.
"""
# The seed/tip url is declared as a constant.
SEED = 'http://info.sjsu.edu/web-dbgen/artic/all-course-to-course.html'
import urllib.request
import bs4
import re

    
def get_links(top_url):
    """
    Enter your docstring here.
    """
    # Extract list of relevant (absolute) links referenced in top_url
    soup = make_soup(top_url)
    tables = soup.find_all('table')
    table = tables[2]
    absolute_links = {urllib.parse.urljoin(top_url, anchor.get('href',
                                                               None)) for
                      anchor in table.find_all('a')}
    return absolute_links


def extract_info(url, course_regex):
    """
    Enter your docstring here.
    """
    # Return college and equivalent course found in the given url if any
    # with urllib.request.urlopen(url) as url_file:
    #     pass
    result = ''
    soup = make_soup(url)
    tables = soup.find_all('table')
    # College name in table('h3')[1]
    table = tables[2]
    college_name = table('h3')[1].get_text()
    print(college_name)


def harvest(all_links, course_regex):
    """
    Enter your docstring here.
    """
    # Invoke extract_url to get the equivalency info for each link in
    # all_links.
    # Join all the equivalency info into a single string (entries must
    # be separated by new line characters).
    for each_link in all_links:
        course = extract_info(each_link, course_regex)
        info = '\n'.join(course)
    return info


def report(info, course_name):
    """
    Enter your docstring here.
    """
    # Write the info harvested to a text file with the name:
    # course_name.txt where course_name is the name as entered by user.
    name = '.'.join([course_name, 'txt'])
    with open(name, 'x', encoding='utf-8') as new_file:
        if not info:
            pass
        else:
            new_file.write(info)
            print(new_file)


def make_soup(url):
    """

    :param url:
    :return:
    """
    try:
        with urllib.request.urlopen(url) as url_file:
            bytes = url_file.read()
    except urllib.error.URLError as url_err:
        print(f'Error opening url: {url}\n{url_err}')
    else:
        soup = bs4.BeautifulSoup(bytes, 'html.parser')
        return soup

def get_info():
    course_name = input('Please enter a course: ')
    return course_name

def read_url(url):
    try:
        with urllib.request.urlopen(url) as url_file:
            bytes = url_file.read()
    except urllib.error.URLError as url_err:
        print(f'Error opening url: {url}\n{url_err}')
    else:
        soup = bs4.BeautifulSoup(bytes,'html.parser')
        for each_style_tag in soup("style"):
            each_style_tag.decompose()
        for each_script_tag in soup("script"):
            each_script_tag.decompose()
        text = soup('h3')[2].get_text()
        return text

def visit_url(url):
    pass


def ok_to_crawl(url):
    pass


def crawl(seed, search_term):
    pass


def main():
    # Get all the relevant links referenced from the seed SEED (top_url)
    for links in get_links(SEED):
        print(links)
    # Prompt the user for a course name
    course_name = get_info()
    # Build a regex corresponding to the course name specified
    # regex: ([A-Za-z]+)\s*(0?\d+[A-Za-z]?) -> cs46b, cs046b, cs 46b,
    # cs 046b, CS 046B, CS46B, CS046B, CS 046B
    course_regex = r"([A-Za-z]+\s*0?\d+[A-Za-z]?)"
    # crawl(SEED, course_regex)
    course_match = re.finditer(course_regex, course_name, re.IGNORECASE)
    for each_match in course_match:
        print('Course: ', each_match.group(1))
        # print('No: ', each_match.group(2))
        # print('Nom: ', each_match.group(3))
    print(course_match)
    # print(extract_info('http://info.sjsu.edu/web-dbgen/artic/SJCITY/course-to'
    #               '-course.html', course_regex))
    # extract_info(SEED, None)
    # Harvest information from all the links
    # info = harvest(links, course_regex)
    # Write the harvested information to the output file
    # report(info, course_name)
    print(f'Your output has been saved in the file: {course_name}.txt')


if __name__ == "__main__":
    main()
