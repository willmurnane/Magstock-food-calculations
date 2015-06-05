from django.conf import settings

def debug_extras(): return {}
if settings.DEBUG:
	def real_debug():
		from django.db import connection
		return connection.queries
	debug_extras = real_debug
	
def addExtraStuff(request):
	return {
		"debug": debug_extras(),
		}
	