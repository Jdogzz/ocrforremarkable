from pdf2image import convert_from_path
import pytesseract
import subprocess
import os
import easyocr
import pdfkit

reader=easyocr.Reader(['en'],gpu=False)
myholderdir="~/scratch/"
docname="Test"
mypdfpath=myholderdir+docname+"-annotations.pdf"
subprocess.call('cd {0} && ~/bin/rmapi geta {1}'.format(myholderdir,docname),shell=True,executable='/bin/bash')
images = convert_from_path(os.path.expanduser(mypdfpath),size=(1404,1872),fmt="jpg")
i=0
myocredtext=""
for image in images:
    #pagetext=pytesseract.image_to_string(image)
    pagetext=" ".join(reader.readtext(image,detail=0))
    print(pagetext)
    if i==0:
        myocredtext=pagetext
    else:
        myocredtext=myocredtext+"\n"+pagetext
    i=i+1
with open(os.path.expanduser(myholderdir+"myocredtext.txt"),"w") as myocredtextfile:
    myocredtextfile.write(myocredtext)
with open(os.path.expanduser(myholderdir+"myocredtext.txt"),"r") as readingfile:
    with open(os.path.expanduser(myholderdir+"myocredtext.html"),"w") as writingfile:
        readingfile = readingfile.read()
        readingfile = readingfile.replace("\n", "<br>")
        writingfile.write(readingfile)
pdfkit.from_file(os.path.expanduser(myholderdir+"myocredtext.html"),os.path.expanduser(myholderdir+"convertedpdf.pdf"))
subprocess.call('cd {0} && ~/bin/rmapi put {0}convertedpdf.pdf /'.format(myholderdir),shell=True,executable='/bin/bash')
