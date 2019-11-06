import re
from django.core.exceptions import ValidationError
"""
This file contains class and method related to cleaning user input
"""
class CleanSummer():
    """
    Assumes the plugin Summernote is being used as a widget for a field called text,
    which this class then implements the cleaning method for
    """
    def clean_text(self):
        """
        Cleans the user input on the text field, and checks maximum length
        
        Returns:
            str : cleaned input
        Raises:
            ValidationError : when text is too long after being cleaned
        """
        data = self.cleaned_data['text']
        max_length = self.summer_max_length
        cleaned = cleanText(data)
        if len(cleaned)>max_length:
            raise ValidationError("This text has length "+str(len(cleaned))+", when the maximum is "+str(max_length))
        return cleaned
#This code was adapted from the summernote-cleaner plugin code (originally written in Javascript)
def cleanText(txt):
    """
    This code removes unnecessary markup from rich text, primarily from malicious purposes such as
    adding scripts or from copying pasting (e.g. Word adds thousands of lines of markup)

    Notes:
        This code was adapted from the Javascript plugin summernote-cleaner (also part of project)
    
    Args:
        txt (str): text to be cleaned
    """
    out = txt
    #sS = /(\n|\r| class=(")?Mso[a-zA-Z]+(")?)/g;
    #out = txt.replace(sS, ' ');
    out = re.sub("(\n|\r| class=\\\"*Mso[a-zA-Z]+\\\"*)"," ",txt)
    #var nL = /(\n)+/g;
    #   out = out.replace(nL, nlO);
    out = re.sub("(\n)+"," ",out) 
    #cS = new RegExp('<!--(.*?)-->', 'gi');
    #     out = out.replace(cS, '');
    out=re.sub("<!--(.*)(meta|link|\\?xml:|st1:|o:|font)(.*)-->"," ",out)
    #  var tS = new RegExp('<(/)*(meta|link|\\?xml:|st1:|o:|font)(.*?)>', 'gi');
    #     out = out.replace(tS, '');
    out=re.sub("<(/)*(meta|link|\\?xml:|st1:|o:|font)([^>]*)>"," ",out)
    bT = ['style', 'script', 'applet', 'embed', 'noframes', 'noscript', 'html']
    for tag in bT:
        #tS = new RegExp('<' + bT[i] + '\\b.*>.*</' + bT[i] + '>', 'gi');
        #out = out.replace(tS, '');
        out=re.sub("<"+tag+"[^>]*>.*</"+tag+">"," ",out)
        #var allowedTags = options.cleaner.keepOnlyTags;
        #if (typeof(allowedTags) == "undefined") allowedTags = [];
        #if (allowedTags.length > 0) {
        #  allowedTags = (((allowedTags||'') + '').toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join('');
        #     var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi;
        #          out = out.replace(tags, function($0, $1) {
        #    return allowedTags.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : ''
        #  });
        #}
    bA = ['style', 'start']
    for attr in bA: 
        #var aS = new RegExp(' ' + bA[ii] + '=[\'|"](.*?)[\'|"]', 'gi');
        #   out = out.replace(aS, '');
        out=re.sub(" "+attr+"=[\\\'|\\\"]([^>]*)[\\\'|\\\"]"," ",out)
    out = re.sub("\<br></p>","</p>",out)
    out = re.sub("<p></p>"," ",out)
    return out

