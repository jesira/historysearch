from datetime import datetime
from django.shortcuts import render
from .models import History
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View

def searchView(request):
    keys = request.GET.get('checkbox_value')
    start = request.GET.get('start_time')
    end = request.GET.get('end_time')

    if keys or (start and end): 
        # print(keys)
        # print(start)
        # print(end)
        if start and end :
            y = History.objects.filter(searched_time__range=(start,end))
        if keys:   
            keys = keys.split(',')
            keys = ' '.join(keys).split()
            user = []
            searched_time = []
            keyword = []
            content = []
            oc = []
            # x= History.objects.none()
            for key in keys:
                if start and end:
                    x = y.filter(Q(keyword__icontains=key)|Q(user__icontains=key)).distinct()
                else:
                    x = History.objects.filter(Q(keyword__icontains=key)|Q(user__icontains=key)).distinct() 
                for i in x:
                    if i.user not in user or i.searched_time not in searched_time or i.keyword not in keyword or i.result not in content:
                        user.append(i.user)        
                        searched_time.append(i.searched_time)
                        keyword.append(i.keyword)
                        content.append(i.result)
                        pat = i.keyword.lower()
                        txt = i.result.lower()
                        oc.append(KMPSearch(pat, txt))
            l = len(user)  
            #print(oc) 
            context = {
                'user' : user,
                'searched_time': searched_time,
                'keyword' : keyword,
                'content' : content,
                'occur' : oc,
                'l' : l ,
            }    
            return JsonResponse(context, status = 200)
    else:
        all_records = History.objects.all()
        #print(all_records)
        return render(request, 'searchform.html', {'all_records': all_records})
 
def KMPSearch(pat, txt): 
    occur = 0
    pattern_length = len(pat) 
    text_length = len(txt)
    lps = [0]*pattern_length
    j = 0 # index for pat[]

    computeLPSArray(pat, pattern_length, lps)
  
    i = 0 # index for txt[]
    while i < text_length:
        if pat[j] == txt[i]:
            i += 1
            j += 1
  
        if j == pattern_length:
            occur += 1
            j = lps[j-1]
  
        # mismatch after j matches
        elif i < text_length and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return occur
  
def computeLPSArray(pat, pattern_length , lps):
    len = 0 # length of the previous longest prefix suffix
  
    lps[0] # lps[0] is always 0
    i = 1
  
    # the loop calculates lps[i] for i = 1 to M-1
    while i < pattern_length:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar 
            # to search step.
            if len != 0:
                len = lps[len-1]
  
                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1
