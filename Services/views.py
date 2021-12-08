# articles/views.py
from .forms import *
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .ML_TEXT.Text_Speech import *


# \main page
class HomePageView(TemplateView):
    template_name = 'Home.html'


# \payment page
class Payment(LoginRequiredMixin, TemplateView):
    template_name = 'services/payment.html'
    
    

# \ extract text from image page
class Image_Text(LoginRequiredMixin, View):
    form_class = ImageForm
    initial = {'key': 'value'}
    template_name = 'services/image_input.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {}
        form = self.form_class(request.POST)
        if len(request.POST['photo']) > 0:
            photo = request.POST['photo']
            context['answer'] = image_to_text(photo)
            return render(request, 'services/image_text_result.html', context)

        return render(request, self.template_name, {'form': form})
    


# \ sumarizes text
class Text_Summary(LoginRequiredMixin, View):
    form_class = SummaryForm
    initial = {'key': 'value'}
    template_name = 'services/summary_input.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {}
        form = self.form_class(request.POST)
        
        if form.is_valid():
            if len(request.POST['textarea']) > 0 and len(request.POST['link']) > 0:
                return redirect('summary')
            
            if len(request.POST['textarea']) >0:
                if request.POST['size']:
                    num_lines = request.POST['size']
                else:
                    num_lines = 5
                content = request.POST['textarea']
                summary = summarizer(content, int(num_lines))
                
                context["original"] = content
                context["summary"] = summary
                return render(request, 'services/original_summary.html', context)
            
            
            elif len(request.POST['link']) >0:
                
                if re.search("(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?", request.POST['link']) == None:
                    return redirect('summary')
                
                else:
                    if request.POST['size']:
                        num_lines = request.POST['size']
                    else:
                        num_lines = 5
                    
                    content, summary = url_summarizer(request.POST['link'], int(num_lines))
                    context["original"] = content
                    context["summary"] = summary
                    return render(request, 'services/original_summary.html', context)
                    
                        
            
            else:
                return redirect('summary')

        return render(request, self.template_name, {'form': form})
        
        
        
# \converts text to audio file
class Text_Audio(LoginRequiredMixin, View):
    form_class = AudioForm
    initial = {'key': 'value'}
    template_name = 'services/audio_paraph.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {}
        form = self.form_class(request.POST)
        
        if form.is_valid():
            if len(request.POST['textarea']) > 0 and len(request.POST['link']) > 0:
                return redirect('audio')
            
            if len(request.POST['textarea']) > 0:
                
                context["summary"] = text_audio(request.POST['textarea'])
                print(context["summary"])
                return render(request, 'services/audio_output.html', context)
            
            
            elif len(request.POST['link']) > 0:
                
                if re.search("(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?", request.POST['link']) == None:
                    return redirect('audio')
                
                else:
                    
                    context["summary"] = text_audio(request.POST['link'], True)
                    return render(request, 'services/audio_output.html', context)
                   
            else:
                return redirect('audio')

        return render(request, self.template_name, {'form': form})
        



# \paraphrases text
class Text_Paraph(LoginRequiredMixin, View):
    form_class = ParaphForm
    initial = {'key': 'value'}
    template_name = 'services/audio_paraph.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {}
        form = self.form_class(request.POST)
        
        if form.is_valid():
            if len(request.POST['textarea']) > 0 and len(request.POST['link']) > 0:
                return redirect('paraph')
            
            if len(request.POST['textarea']) > 0:
                context["summary"] = sentiment_analysis(request.POST['textarea'])
                context["original"] = request.POST['textarea']
                
                return render(request, 'services/original_summary.html', context)
            
            
            elif len(request.POST['link']) > 0:
                
                if re.search("(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?", request.POST['link']) == None:
                    return redirect('paraph')
                
                else:
                    answer, text = sentiment_analysis(request.POST['link'], link=True)
                    context["summary"] = answer
                    context["original"] = text
                    
                    return render(request, 'services/original_summary.html', context)
                   
            else:
                return redirect('paraph')

        return render(request, self.template_name, {'form': form})