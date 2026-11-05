import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
def plate(cut, out, circle, right, bottom, h, minx):
    W,H=1080,1350
    cv=Image.new('RGBA',(W,H),(0,0,0,0))
    cx,cy,r=circle
    # mint circle
    c=Image.new('RGBA',(W,H),(224,241,236,0)); m=Image.new('L',(W,H),0)
    ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255); c.putalpha(m); cv=Image.alpha_composite(cv,c)
    dr=Image.open(cut).convert('RGBA')
    dr=dr.crop(dr.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox())
    dr=dr.resize((round(dr.width*h/dr.height),h),Image.LANCZOS)
    rgb,a=dr.convert('RGB'),dr.getchannel('A')
    a=a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    arr=np.asarray(rgb).astype(np.float32)
    # colour-match to the mint/green scene: tiny cool-green cast, gentle light falloff left->right
    arr[...,0]*=0.98; arr[...,1]*=1.01; arr[...,2]*=1.00
    arr*=np.linspace(1.04,0.93,arr.shape[1])[None,:,None]
    rgb=Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    A=np.asarray(a).astype(np.float32); hh,ww=A.shape
    low=A[int(hh*0.6):]; lx=int(np.argmax((low>128).any(axis=0)))
    cols=np.ones(ww,np.float32); cols[lx:lx+110]=np.linspace(0,1,110)**0.8
    m=np.ones((hh,ww),np.float32); y0=int(hh*0.55)
    m[y0:,:]=cols[None,:]; m[y0-40:y0,:]=1-(1-cols[None,:])*np.linspace(0,1,40)[:,None]
    a=Image.fromarray((A*m).astype(np.uint8))
    px=right-dr.width; py=bottom-h
    assert px>=minx, (px,minx)
    # soft green glow + contact shadow behind him, inside the circle
    gl=Image.new('L',(W,H),0); ImageDraw.Draw(gl).ellipse([px+30,py+40,px+dr.width-30,py+h+80],fill=150)
    glow=Image.new('RGBA',(W,H),(98,170,148,0)); glow.putalpha(gl.filter(ImageFilter.GaussianBlur(90)))
    cv=Image.alpha_composite(cv,glow)
    sh=Image.new('L',(W,H),0); sh.paste(a.point(lambda v:int(v*0.35)),(px+18,py+14))
    shadow=Image.new('RGBA',(W,H),(13,44,92,0)); shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(22)))
    cv=Image.alpha_composite(cv,shadow)
    dr=rgb.copy(); dr.putalpha(a)
    edge=ImageChops.subtract(a,a.filter(ImageFilter.MinFilter(9))).filter(ImageFilter.GaussianBlur(4))
    rim=Image.new('RGBA',dr.size,(235,250,244,0))
    ra=np.asarray(edge).astype(np.float32)*np.linspace(1.0,0.2,dr.width)[None,:]*1.1
    rim.putalpha(Image.fromarray(np.clip(ra,0,255).astype(np.uint8)))
    for lay in (dr,rim):
        L=Image.new('RGBA',(W,H),(0,0,0,0)); L.alpha_composite(lay,(px,py)); cv=Image.alpha_composite(cv,L)
    cv.save(out); print(out,'person x',px,'-',px+dr.width,'y',py,'-',bottom)
plate('dr-three-quarter_cut.png','cover_plate.png',(860,700,390),1160,1200,720,505)
plate('dr-front_cut.png','s10_plate.png',(880,600,340),1140,1080,760,530)
