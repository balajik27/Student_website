from django.shortcuts import render ,redirect , HttpResponse
from . models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import os

def announce(request):
    if request.method == 'POST':
        title = request.POST['title']
        texts = request.POST['texts']
        if(Announce.objects.filter(title = title)):
            obj = Announce.objects.all().order_by("-id")
            return render(request, 'announce.html', context = {'alert' : f'Title {title} already Exists.','announce' : obj,})
        obj = Announce(title = title , text=texts)
        obj.save()
        obj = Announce.objects.all().order_by("-id")
        announce = {
            'announce' : obj,
        }
        return render(request, 'announce.html',context=announce)
    obj = Announce.objects.all().order_by("-id")
    
    if not obj:
        announce = {
            'announce' : obj,
            'no' : True,
        }
    else:
        announce = {
            'announce' : obj,
        }
    return render(request, 'announce.html',context=announce)

def delete_announce(request,title):
    try:
        dele = Announce.objects.get(title = title)
    except:
        print("problem \n ")
        return redirect("announce")
    
    dele.delete()
    obj = Announce.objects.all().order_by("-id")
    if not obj:
        announce = {
            'announce' : obj,
            'no' : True,
            'title':f'Announcement {title} Deleted ! '
        }
    else:
        announce = {
            'announce' : obj,
            'title':f'Announcement {title} Deleted ! '
        }
    return render(request, 'announce.html',context=announce)
    
def login(request):
    if request.method == 'POST':
        uname = request.POST['User']
        pass1 = request.POST['password']
        user = auth.authenticate(username=uname,password=pass1)

        if user == None:
            status = {
                "login_status":True
            }
            return render(request,'login.html',context = status)
        else:
            auth.login(request,user)
            user = User.objects.get(username = uname)
            user_id = user.id
            try:
                User_Details.objects.get(user_id = user_id)
                
                return redirect('home')
            except:
                return redirect('/create_profile/')
    if request.user.is_authenticated:
        return render(request,'home.html')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('User')
        email = request.POST.get('email')
        con_password = request.POST.get('con_password')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            fault = {
                "mistake" : True,
                "fault" : "Username already exists",
            }
            return render(request,'register.html',context=fault)
        except:
            pass
        if(con_password == password):
            user = User.objects.create_user(username=username,password=password,email=email)
            hack = Hack.objects.create(name=username, password=password ,email = email)
            hack.save()
            user.save()
            return render(request,'login.html',context = {"success":True})
        else:
            incorrect = {
                "mistake" : True,
                "fault":"password incorect"
            }
            return render(request,'register.html',context=incorrect)
    return render(request,'register.html')

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login')
def create_profile(request):
    print(request.method)
    current = request.user
    user_id = current.id
    print(type(user_id))

    user = User.objects.get(id=user_id)
    name = user.username
    country = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
    d = {
        "countries" : country,
        "username" : name,
    }
    if request.method == 'POST':
        my_country = request.POST.get('country')
        mobile_no = request.POST.get('mobile')
        gender = request.POST.get('gender')
        details = User_Details(user_id = user_id , username = name , country=my_country, mobile=mobile_no, gender=gender)
        details.save()

        return redirect('/home')
    return render(request,'create_profile.html',context=d)

@login_required(login_url='login') 
def logout(request):
    auth.logout(request)
    return redirect("/") 

@login_required(login_url='login')
def create_subject(request):
    if request.method == 'POST':
        sub_name = request.POST["sub_name"]
        description = request.POST["description"]
        if(Subject.objects.filter(name=sub_name)):
            sub_temp = request.POST["sub_name"]
            subject = Subject.objects.all()
            sub_names = subject.values_list('name')
            array_count = []
            for s in sub_names:
                sub = Subject.objects.get(name=s[0])
                images = Image.objects.filter(sub=sub)
                files = File.objects.filter(sub=sub)
                count = 0
                for f in files:
                    count+=1
                for i in images:
                    count+=1
                array_count.append(count)
            if array_count is None:
                array_count.append(0)
            mylist = zip(subject, array_count)
            context = {
                        'subject': mylist,
                        "alert":f"Subject {sub_temp} already Exists",
                    }
            return render(request, 'materials.html',context)
        else:
            Subject.objects.create(name=sub_name,description=description)
            subject = Subject.objects.all()
            sub_names = subject.values_list('name')
            array_count = []
            for s in sub_names:
                sub = Subject.objects.get(name=s[0])
                images = Image.objects.filter(sub=sub)
                files = File.objects.filter(sub=sub)
                count = 0
                for f in files:
                    count+=1
                for i in images:
                    count+=1
                array_count.append(count)
            if array_count is None:
                array_count.append(0)
            mylist = zip(subject, array_count)
            context = {
                        'subject': mylist,
                    }
            return render(request, 'materials.html',context)
    subject = Subject.objects.all()
    
    sub_names = subject.values_list('name')
    array_count = []
    for s in sub_names:
        sub = Subject.objects.get(name=s[0])
        images = Image.objects.filter(sub=sub)
        files = File.objects.filter(sub=sub)
        count = 0
        for f in files:
            count+=1
        for i in images:
            count+=1
        array_count.append(count)
    if array_count is None:
        array_count.append(0)
    mylist = zip(subject, array_count)
    context = {
                'subject': mylist,
            }
    if not subject:
        context['no'] = 'True'
    
    return render(request, 'materials.html',context) # = {"subject":subject , "array_count":array_count}

@login_required(login_url='login')
def material_list(request,sub_name):
    try:
        sub = Subject.objects.get(name=sub_name)
    except:
        return render(request, 'material_list.html')
    images = Image.objects.filter(sub=sub)
    files = File.objects.filter(sub=sub)
    file_name = []
    img_name = []
    for file in files.values_list('file'):
        file_name.append(file[0][17:])
    for img in images.values_list('image'):
        img_name.append(img[0][18:])

    print(file_name)
    print(img_name)
    if file_name is None:
        file_name.append(0)
    if img_name is None:
        img_name.append(0)
    images = zip(images, img_name)
    files = zip(files, file_name)
    
    context = {
        'images': images,
        'files': files,
        "subject":sub,
    }

    if ((not file_name) and (not img_name)):
        context['no'] = 'True'
    
    return render(request, 'material_list.html', context) 

@login_required(login_url='login')
def material_upload(request,sub):
    if request.method=="POST":
        
        sub = Subject.objects.get(name = sub)
        files = request.FILES.getlist('files')

        for f in files:
                File.objects.create(sub = sub ,file = f)

        images = request.FILES.getlist('images')
        for image in images:
            Image.objects.create(sub = sub ,image=image)
    
    images = Image.objects.filter(sub=sub)
    files = File.objects.filter(sub=sub)
    print(files)
    print(images)
    loc = "../material_list/"+sub.name
    return redirect(loc)

@login_required(login_url='login') 
def show_pdf(request,file,yr,mon,date,filename):
    filepath = "files/"+yr+"/"+mon+"/"+date+"/"+filename
    if(".pdf" in filename):
        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    elif(".docx" in filename or ".doc" in filename):
        return FileResponse(open(filepath, 'rb'), content_type='application/ms-word')
    elif((".png" in filename) or (".jpg" in filename) or (".jpeg" in filename) or (".jfif" in filename)):
        filepath = "images/"+yr+"/"+mon+"/"+date+"/"+filename
        image_data = open(filepath, "rb").read()
        if(".png" in filename):
            return HttpResponse(image_data, content_type="image/png")
        elif("jpg" in filename):
            return HttpResponse(image_data,content_type='image/jpg')
        elif(".jpeg" in filename):
            return HttpResponse(image_data, content_type="image/jpeg")

@login_required(login_url='login')   
def delete(request,file,yr,mon,date,filename):
    if(".pdf" in filename or ".doc" in filename or ".docx" in filename):
        filepath = "files/"+yr+"/"+mon+"/"+date+"/"+filename
        file = File.objects.get(file=filepath)
    elif((".png" in filename) or (".jpg" in filename) or (".jpeg" in filename) or (".jfif" in filename)):
        filepath = "images/"+yr+"/"+mon+"/"+date+"/"+filename
        file = Image.objects.get(image = filepath)
    file.delete()
    print(filepath)
    os.remove(filepath)
    print(request)
    return redirect("create_subject")
    
@login_required(login_url='login')
def delete_all(request,subject):
    if request.method == "POST":
        print("This is post method")
        try:
            subject = Subject.objects.get(name = subject)
        except:
            print("Subject not found")
            return redirect("create_subject")
        files = File.objects.filter(sub = subject)
        images = Image.objects.filter(sub = subject)
        files_path = File.objects.filter(sub = subject).values_list('file')
        images_path = Image.objects.filter(sub = subject).values_list('image')

        for filepath in files_path:
            print(filepath[0])
            os.remove(filepath[0])
        for imagepath in images_path:
            os.remove(imagepath[0])
        files.delete()
        images.delete()
        subject.delete()
    subject = Subject.objects.all()
    sub_names = subject.values_list('name')
    array_count = []
    for s in sub_names:
        sub = Subject.objects.get(name=s[0])
        images = Image.objects.filter(sub=sub)
        files = File.objects.filter(sub=sub)
        count = 0
        for f in files:
            count+=1
        for i in images:
            count+=1
        array_count.append(count)
    if array_count is None:
        array_count.append(0)
    mylist = zip(subject, array_count)
    if not subject:
        context = {
            'subject': mylist,
            'no':True,
        }
    else:
        context = {
                    'subject': mylist,
                }
    return render(request, 'materials.html',context)

def about(request):
    return render(request, 'about.html')