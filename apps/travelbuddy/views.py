from django.shortcuts import render, redirect , HttpResponse
from .models import Users, Trips, Join
from django.contrib import messages

# Create your views here.
def index(request):
	# request.session.clear()
	return render(request, 'travelbuddy/index.html')

def insert(request):
	if request.method == "POST":
		result = Users.registerMgr.register(request.POST['name'],request.POST['username'],request.POST['password'],request.POST['confirm_password'])
		# print "result===",result
	 	if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/travels')
	 	else:
	 		# print result[0], "="*20
	 		for x in xrange(len(result[1])):
	 			print x
	 			messages.error(request, result[1][x])

	 		return redirect('/')

def login(request):
	if request.method == "POST":
		result = Users.loginMgr.login(request.POST['username_login'],request.POST['password_login'])
		login = Users.loginMgr.filter(username=request.POST['username_login'])
		trips = Trips.tripsMgr.all()

		users = Users.registerMgr.all()
		if len(login)> 0:
			login = login[0].id, login[0].name
			request.session['user_id'] = login
		if result[0]:
	 		# print result[0], "="*20,result[1].name
	 		request.session['name'] = result[1].name
	 		request.session['user_id'] = result[1].id
	 		return redirect('/travels')
	 	else:
	 		# print result[0], "="*20
	 		# request.session['message'] =result[1]
	 		for x in xrange(len(result[1])):
	 			print x
	 			messages.error(request, result[1][x])
	 		return redirect('/')

def trips(request):
	trip = Trips.tripsMgr.filter(user_id=request.session['user_id'])
	joins = Join.joinsMgr.filter(user_id=request.session.get('user_id'))
	trips_other = Trips.tripsMgr.exclude(user_id=request.session['user_id'])
	for x in joins:
		trips_other = trips_other.exclude(id = x.trip.id)

	# print '='*50, request.session.get('user_id')
	context = {
	'joins': joins,
	'trip' : trip,
	'trips_other': trips_other
	}
	return render(request, 'travelbuddy/travels.html',context)
		
	
def success(request):
	result = Users.registerMgr.all()

	context = {
			'result': result,
			'name' : request.session.get('name')
			}
	return render(request, 'travelbuddy/travels.html',context)

def delete(request, id):
	#join.joinsMgr.all().delete()
	Join.joinsMgr.filter(trip_id=id).delete()
	return redirect('/travels')

def add_trips(request):
	if request.method == "GET": 
		# print "Session === user_id====",type(request.session.get('user_id')[0])
		return render(request, 'travelbuddy/add.html')
	elif request.method == "POST":
			print "USER_ID++++++++++",request.session.get('user_id')
			print 
			trips = Trips.tripsMgr.add(destination=request.POST['txt_destination'],description=request.POST['txt_description'],travel_from=request.POST['txt_date_from'],travel_to=request.POST['txt_date_to'])

			if trips[0]:
				trips = Trips.tripsMgr.create(destination=request.POST['txt_destination'],description=request.POST['txt_description'],user_id =request.session.get('user_id') ,travel_from=request.POST['txt_date_from'],travel_to=request.POST['txt_date_to'])
				trips.save()
				print trips.id, "="*100
				join = Join.joinsMgr.create(trip_id=trips.id, user_id=request.session.get('user_id'))
				
				return redirect('/travels')
			else:
				print "FALSE"
				for x in xrange(len(trips[1])):
					print x
					messages.error(request, trips[1][x])
				return redirect('/travels/add')

def user_destination(request, id):
	trip = Trips.tripsMgr.filter(id=id)
	join = Join.joinsMgr.filter()
	user= Users.registerMgr.all()
	context = {
	'trip':trip,
	'join': join,
	'user':user
	}
	return render(request , 'travelbuddy/user_detail.html', context)

def logout(request):
	# Trips.tripsMgr.all().delete()
	request.session.pop('user_id')
	request.session.pop('name')
	# Join.joinsMgr.all().delete()
	return render(request, 'travelbuddy/index.html')


def join(request, id):
	if request.method == "GET":
		# print "USER_ID===========" ,request.session.get('user_id')
		trip = Trips.tripsMgr.filter(id=id)
		check_trip_id = int(id)
		# print "JOin Count ===========", Join.joinsMgr.all().count()

		if Join.joinsMgr.all().count() == 0:
			result = Join.joinsMgr.create(user_id=request.session.get('user_id'),trip_id=check_trip_id)
			result.save()
			messages.error(request, 'Congratulation!! You have joined')
			return redirect('/travels')
			# return HttpResponse("Congratulation!! You have joined")
		elif Join.joinsMgr.all().count() > 0:
			join = Join.joinsMgr.filter(trip_id=check_trip_id).filter(user_id=request.session.get('user_id'))
			# join_user = Join.joinsMgr.filter(user_id=request.session.get('user_id'))
			if len(join)> 0 :
				join = join[0].trip_id, join[0].user_id
				# print "Join trip_id ======",join[0],"Join user_id ======", join[1]
				if join[0] == check_trip_id and join[1] == request.session.get('user_id'):					
					# print "Trip_ID====",join[0], "_TRIP_ID=====", check_trip_id, "user_id=====",join[1],"user_id_form",request.session.get('user_id')
					messages.error(request, 'You already joined this trip!!')
				return redirect('/travels')
				# return HttpResponse("You already joined this trip!!")
			else: 
				result = Join.joinsMgr.create(user_id=request.session.get('user_id'),trip_id=check_trip_id)
				result.save()
				messages.error(request, 'Congratulation!! You have joined')
				return redirect('/travels')
				# return HttpResponse("Congratulation!! You have joined")
	else:
		return redirect('/')

def remove_join(request, trip_id, id):
	Join.joinsMgr.filter(trip_id=trip_id).filter(user_id=id).delete()
	return redirect('/travels')




			

		