from bottle import route, request, response, run
@route('/get')
def display_forum():
    forum_id = request.GET.get('id')
    page = request.GET.get('page', '1')
    return 'Forum ID: %s (page %s)' % (forum_id, page)

run()
