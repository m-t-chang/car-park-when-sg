from django.http import HttpResponse


def index(request):
    # members = Members.objects.all()[1:20]  # example of slicing
    # output = ', '.join([member.name for member in members])
    # return HttpResponse(output)
    return HttpResponse('hello world')
