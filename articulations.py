# ----------------------------------------------------------------------
# Name:     articulations
# Purpose:  Homework 9
#
# Author(s): Kiwibud
#
# ----------------------------------------------------------------------
"""
 A program to harvest all college equivalent courses to a SJSU course

 Compile SJSU course articulation information from multiple web pages
 Save that information in a text file on the user's computer
"""
import urllib.request
import bs4
import re
# The seed/tip url is declared as a constant.
SEED = 'http://info.sjsu.edu/web-dbgen/artic/all-course-to-course.html'
COURSE_ID_LEN = 4


def get_links(top_url):
    """
    Extract list of relevant (absolute) links referenced in top_url
    :param top_url: (string) given url link to extract relevant links
    :return: (list) list of absolute links
    """
    soup = make_soup(top_url)
    tables = soup.find_all('table')
    table = tables[2]
    absolute_links = [urllib.parse.urljoin(top_url, anchor.get('href',
                                                               None)) for
                      anchor in table.find_all('a')]
    return absolute_links


def extract_info(url, course_regex):
    """
    Return college and equivalent course found in the given url if any
    :param url: (string) given url to get information from
    :param course_regex: (string) given regex to find matched info
    :return: (string) college name and equivalent courses or None
    """
    # Return college and equivalent course found in the given url if any
    soup = make_soup(url)
    tables = soup.find_all('table')
    info_table = tables[2]
    college_name = info_table('h3')[1].get_text()
    regex = re.compile(course_regex + r'.*', re.IGNORECASE)
    sjsu_rows = info_table.find_all('td', string=regex)
    for each_row in sjsu_rows:
        equivalent_col = (each_row.find_next_sibling('td')) \
            .find_next_sibling('td')
        course_info = equivalent_col.get_text(separator=' ')
        course_info = ' '.join(course_info.split())
        if re.match('No', course_info) is None:
            return f'{college_name}: {course_info}'


def harvest(all_links, course_regex):
    """
    Get the equivalent info for each link in all links
    :param all_links: (list) list of links
    :param course_regex: (string) regex that defines course patterns
    :return: (string) all equivalent courses correspond to course_regex
    """
    # Invoke extract_url to get the equivalency info for each link in
    # all_links.
    # Join all the equivalency info into a single string (entries must
    # be separated by new line characters).
    info = ''
    for each_link in all_links:
        course_info = extract_info(each_link, course_regex)
        if course_info is not None:
            print(course_info)
            info += f'{course_info}\n'
    return info


def report(info, course_name):
    """
    Write the info harvested to a text file named as course_name
    :param info: (string) harvested information
    :param course_name: (string) name entered by user
    :return: None
    """
    # Write the info harvested to a text file with the name:
    # course_name.txt where course_name is the name as entered by user.
    name = '.'.join([course_name, 'txt'])
    with open(name, 'w', encoding='utf-8') as new_file:
        new_file.write(info)
        # print(new_file)


def make_soup(url):
    """
    Parse the specified html file.
    :param url: (string) url link to be parsed
    :return: BeautifulSoup object
    """
    try:
        with urllib.request.urlopen(url) as url_file:
            page = url_file.read()
    except urllib.error.URLError as url_err:
        print(f'Error opening url: {url}\n{url_err}')
    else:
        soup = bs4.BeautifulSoup(page, 'html.parser')
        return soup


def course_variation(course_name):
    """
    Formalize a regex to fix all the variations from user's input
    :param course_name: name of course
    :return: Formalized course_regex to find the course info
    """
    pattern = r'([A-Za-z]+)(\s*)(\d+)(\s*)([A-Za-z]?)'
    course_match = re.finditer(pattern, course_name, re.IGNORECASE)
    if not course_match:
        print("Course name does not match SJSU pattern")
        return None
    else:
        for each_match in course_match:
            subject = each_match.group(1)
            course_num = each_match.group(3)
            course_letter = each_match.group(5)
            return subject + r' 0*' + course_num + course_letter


def main():
    # Get all the relevant links referenced from the seed SEED (top_url)
    links = get_links(SEED)
    # Prompt the user for a course name
    course_name = input('Please enter a course: ')
    # Build a regex corresponding to the course name specified
    course_regex = course_variation(course_name)
    print(f'course_regex: {course_regex}')
    # Harvest information from all the links
    info = harvest(links, course_regex)
    # Write the harvested information to the output file
    report(info, course_name)
    print(f'Your output has been saved in the file: {course_name}.txt')


if __name__ == "__main__":
    main()
