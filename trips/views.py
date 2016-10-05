from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from trips.models import Post
from trips.models import Article
import os
import subprocess, sys
import multiprocessing
from subprocess import Popen, PIPE, STDOUT
from django import forms
import chatbot
import random

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['frontId', 'content', ]

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['iden', 'content', ]
def creates(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
			Post.objects.create(iden=new_article.title,content=new_article.content)
			return HttpResponseRedirect('/index/'+new_article.title)

	form = ArticleForm()
	return render(request, 'create_article.html', {'form': form})

def index(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		new_article = form.save()
		if form.is_valid():
			global output
			output = chatb.listen(new_article.content)
			if new_article.frontId == '':
				while(1):
					myid = random.randint(0,99)
					post = Post.objects.filter(iden=myid)
					if len(post) == 0:
						break
				Post.objects.create(iden=myid,content=output[1])
				#print(str(myid)+'#'+output[0])
				return render(request, 'get.html', {'form': form,'data': output[0]})
			else:
				post = Post.objects.filter(iden=new_article.frontId)
				if len(post) == 0:
					print('your Id have ERROR!!')
					return render(request, 'get.html', {'form': form,'data': 'your Id have ERROR!!'})
				else:
					if output[0] not in Post.objects.get(iden=new_article.frontId).content.split('#'):
						Post.objects.filter(iden=new_article.frontId).update(content=output[1])
					#print(Post.objects.get(iden=new_article.frontId).content.split('#'))
						pass
					return render(request, 'get.html', {'form': form,'data': new_article.frontId+'#'+output[0]})
		#	process.stdin.write(str.encode(new_article.content))
		#	stdo = process.communicate(input=(new_article.content).encode())[0]
		#	print(process.stdout.readline())
		#	process.stdout.close()
	global chatb
	form = ArticleForm()
	chatb = chatbot.Chatbot()
	
	#process = Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE)
	#for line in iter(process.stdout.readline,''):
	#	print("test:", line.rstrip())
	#	if line.rstrip() == b'[Console] Initialized successfully :>':
	#		print("I am break")
	#		break
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'create_article.html', {'form': form})


def request_data(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
	#		print(process.stdout.readline())
	#		process.stdout.close()
			return render(request, 'get.html', {'form': form,'data': new_article.content})

	form = ArticleForm()
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'get.html', {'form': form})
	
def submit(request, pk, data):
	print(pk)
	print(data)
	post = Post.objects.filter(iden=pk)
	if len(post) == 0:
		Post.objects.create(iden=pk,content=data)
	return render(request, 'submit.html', {'post': pk,'data': data})