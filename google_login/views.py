from django.shortcuts import render

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("https://project-1-34.herokuapp.com/")