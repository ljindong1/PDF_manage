def get_print_pages(page_string):
    pages = []
    ranges = page_string.split(',')  # 쉼표를 기준으로 페이지 번호들을 분리합니다.

    for item in ranges:
        if '-' in item:
            start, end = map(int, item.split('-'))
            pages.extend(range(start, end + 1))  # 범위의 페이지 번호들을 추가합니다.
        else:
            pages.append(int(item))  # 단일 페이지 번호를 추가합니다.

    return pages

page_string = "1,3,7-10"
print_pages = get_print_pages(page_string)
print(print_pages)