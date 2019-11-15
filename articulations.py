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

COURSE_ID_LEN = 4


def get_links(top_url):
    """
    Enter your docstring here.
    """
    # Extract list of relevant (absolute) links referenced in top_url
    soup = make_soup(top_url)
    tables = soup.find_all('table')
    table = tables[2]
    absolute_links = [urllib.parse.urljoin(top_url, anchor.get('href',
                                                               None)) for
                      anchor in table.find_all('a')]
    return absolute_links


def extract_info(url, course_regex):
    """
    Enter your docstring here.
    """
    # Return college and equivalent course found in the given url if any
    soup = make_soup(url)
    tables = soup.find_all('table')
    info_table = tables[2]
    college_name = info_table('h3')[1].get_text()
    regex = re.compile(course_regex + r'.*', re.IGNORECASE)
    sjsu_rows = info_table.find_all('td', string=regex)
    course_info = 'hi'
    for each_row in sjsu_rows:
        equivalent_col = (each_row.find_next_sibling('td')) \
            .find_next_sibling('td')
        course_info = equivalent_col.get_text(separator=' ')
        course_info = ' '.join(course_info.split())
        if re.match('No', course_info) is None:
            return f'{college_name}: {course_info}'


def harvest(all_links, course_regex):
    """
    Enter your docstring here.
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
            info = '\n'.join(course_info)
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
    pattern = r'([A-Za-z]+)(\s*)(0?)(\d+)([A-Za-z]?)'
    course_match = re.finditer(pattern, course_name, re.IGNORECASE)
    if not course_match:
        print("Course name not matching pattern")
        return None
    else:
        for each_match in course_match:
            subject = each_match.group(1)
            course_num = each_match.group(4)
            course_letter = each_match.group(5)
            # print(f'subject: {subject}  courseID {course_num} {course_letter}')
            if len(course_num) < 3:
                # print('add 0')
                return subject + r' 0' + course_num + course_letter
            else:
                print('no adding 0')
                return subject + r' ' + course_num + course_letter


def main():
    # Get all the relevant links referenced from the seed SEED (top_url)
    links = get_links(SEED)
    # for links in get_links(SEED):
    #     print(type(links))
    #     print(links)
    # Prompt the user for a course name
    course_name = input('Please enter a course: ')
    # Build a regex corresponding to the course name specified
    course_regex = course_variation(course_name)
    print(f'course_regex: {course_regex}')
    # Harvest information from all the links
    info = harvest(links, course_regex)
    # Write the harvested information to the output file
    report(info, course_name)
    print(f'Your output has been saved in the file: {course_regex}.txt')


if __name__ == "__main__":
    main()
