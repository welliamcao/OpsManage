/**
 * Copyright (C) 2010-2011 Graham Breach
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
/**
 * jQuery.tagcanvas 1.11.1
 * For more information, please contact <graham@goat1000.com>
 */
(function($) {
var i, j, abs = Math.abs, sin = Math.sin, cos = Math.cos, hexlookup3 = {}, hexlookup2 = {}, hexlookup1 = {
	0:"0,",   1:"17,",  2:"34,",  3:"51,",  4:"68,",  5:"85,",
	6:"102,", 7:"119,", 8:"136,", 9:"153,", a:"170,", A:"170,",
	b:"187,", B:"187,", c:"204,", C:"204,", d:"221,", D:"221,",
	e:"238,", E:"238,", f:"255,", F:"255,"	
}, Oproto, Tproto, TCproto, doc = document;
for(i = 0; i < 256; ++i) {
	j = i.toString(16);
	if(i < 16)
		j = '0' + j;
	hexlookup2[j] = hexlookup2[j.toUpperCase()] = i.toString() + ',';
}
function Defined(d) {
	return typeof(d) != 'undefined';
}
function PointsOnSphere(n) {
	var i, y, r, phi, pts = [], inc = Math.PI * (3-Math.sqrt(5)), off = 2/n;
	for(i = 0; i < n; ++i) {
		y = i * off - 1 + (off / 2);
		r = Math.sqrt(1 - y*y);
		phi = i * inc;
		pts.push([cos(phi)*r, y, sin(phi)*r]);
	}
	return pts;
}
function Cylinder(n,o,i,j,k,l) {
	var phi, pts = [], inc = Math.PI * (3-Math.sqrt(5)), off = 2/n;
	for(i = 0; i < n; ++i) {
		j = i * off - 1 + (off / 2);
		phi = i * inc;
		k = cos(phi);
		l = sin(phi);
		pts.push(o ? [j, k, l] : [k, j, l]);
	}
	return pts;
}
function PointsOnCylinderV(n) { return Cylinder(n) }
function PointsOnCylinderH(n) { return Cylinder(n,1) }
function SetAlpha(c,a) {
	var d = c, p1, p2, ae = (a*1).toPrecision(3) + ')';
	if(c[0] === '#') {
		if(!hexlookup3[c])
			if(c.length === 4)
				hexlookup3[c] = 'rgba(' + hexlookup1[c[1]] + hexlookup1[c[2]] + hexlookup1[c[3]];
			else
				hexlookup3[c] = 'rgba(' + hexlookup2[c.substr(1,2)] + hexlookup2[c.substr(3,2)] + hexlookup2[c.substr(5,2)];
		d = hexlookup3[c] + ae;
	} else if(c.substr(0,4) === 'rgb(' || c.substr(0,4) === 'hsl(') {
		d = (c.replace('(','a(').replace(')', ',' + ae));
	} else if(c.substr(0,5) === 'rgba(' || c.substr(0,5) === 'hsla(') {
		p1 = c.lastIndexOf(',') + 1, p2 = c.indexOf(')');
		a *= parseFloat(c.substring(p1,p2));
		d = c.substr(0,p1) + a.toPrecision(3) + ')';
	}
	return d;
}
function NewCanvas(w,h) {
	// if using excanvas, give up now
	if(window.G_vmlCanvasManager)
		return null;
	var c = doc.createElement('canvas');
	c.width = w;
	c.height = h;
	return c;
}
function ShadowAlphaBroken() {
	var cv = NewCanvas(3,3), c, i;
	if(!cv)
		return false;
	c = cv.getContext('2d');
	c.strokeStyle = '#000';
	c.shadowColor = '#fff';
	c.shadowBlur = '3';
	c.globalAlpha = 0;
	c.strokeRect(2,2,2,2);
	c.globalAlpha = 1;
	i = c.getImageData(2,2,1,1);
	cv = null;
	return (i.data[0] > 0);
}
function FindGradientColour(t,p) {
	var l = 1024, g = t.weightGradient, cv, c, i, gd, d;
	if(t.gCanvas) {
		c = t.gCanvas.getContext('2d');
	} else {
		t.gCanvas = cv = NewCanvas(l,1);
		if(!cv)
			return null;
		c = cv.getContext('2d');
		gd = c.createLinearGradient(0,0,l,0);
		for(i in g)
			gd.addColorStop(1-i, g[i]);
		c.fillStyle = gd;
		c.fillRect(0,0,l,1);
	}
	d = c.getImageData(~~((l-1)*p),0,1,1).data;
	return 'rgba(' + d[0] + ',' + d[1] + ',' + d[2] + ',' + (d[3]/255) + ')';
}
function TextSet(c,f,l,s,sc,sb,so) {
	var xo = (sb || 0) + (so && so[0] < 0 ? abs(so[0]) : 0),
		yo = (sb || 0) + (so && so[1] < 0 ? abs(so[1]) : 0);
	c.font = f;
	c.textBaseline = 'top';
	c.fillStyle = l;
	sc && (c.shadowColor = sc);
	sb && (c.shadowBlur = sb);
	so && (c.shadowOffsetX = so[0], c.shadowOffsetY = so[1]);
	c.fillText(s, xo, yo);
}
function TextToCanvas(s,f,ht,w,h,l,sc,sb,so) {
	var cw = w + abs(so[0]) + sb + sb, ch = h + abs(so[1]) + sb + sb, cv, c;
	cv = NewCanvas(cw,ch);
	if(!cv)
		return null;
	c = cv.getContext('2d');
	TextSet(c,f,l,s,sc,sb,so);
	return cv;
}
function AddShadowToImage(i,sc,sb,so) {
	var cw = i.width + abs(so[0]) + sb + sb, ch = i.height + abs(so[1]) + sb + sb, cv, c,
		xo = (sb || 0) + (so && so[0] < 0 ? abs(so[0]) : 0),
		yo = (sb || 0) + (so && so[1] < 0 ? abs(so[1]) : 0);
	cv = NewCanvas(cw,ch);
	if(!cv)
		return null;
	c = cv.getContext('2d');
	sc && (c.shadowColor = sc);
	sb && (c.shadowBlur = sb);
	so && (c.shadowOffsetX = so[0], c.shadowOffsetY = so[1]);
	c.drawImage(i, xo, yo);
	return cv;
}
function FindTextBoundingBox(s,f,ht) {
	var w = parseInt(s.length * ht), h = parseInt(ht * 2), cv = NewCanvas(w,h), c, idata, w1, h1, x, y, i, ex;
	if(!cv)
		return null;
	c = cv.getContext('2d');
	c.fillStyle = '#000';
	c.fillRect(0,0,w,h);
	TextSet(c,ht + 'px ' + f,'#fff',s)

	idata = c.getImageData(0,0,w,h);
	w1 = idata.width; h1 = idata.height;
	ex = {
		min: { x: w1, y: h1 },
		max: { x: -1, y: -1 }
	};
	for(y = 0; y < h1; ++y) {
		for(x = 0; x < w1; ++x) {
			i = (y * w1 + x) * 4;
			if(idata.data[i+1] > 0) {
				if(x < ex.min.x) ex.min.x = x;
				if(x > ex.max.x) ex.max.x = x;
				if(y < ex.min.y) ex.min.y = y;
				if(y > ex.max.y) ex.max.y = y;
			}
		}
	}
	// device pixels might not be css pixels
	if(w1 != w) {
		ex.min.x *= (w / w1);
		ex.max.x *= (w / w1);
	}
	if(h1 != h) {
		ex.min.y *= (w / h1);
		ex.max.y *= (w / h1);
	}

	cv = null;
	return ex;
}
function FixFont(f) {
	return "'" + f.replace(/(\'|\")/g,'').replace(/\s*,\s*/g, "', '") + "'";
}
function AddHandler(h,f,e) {
	e = e || doc;
	if(e.addEventListener)
		e.addEventListener(h,f,false);
	else
		e.attachEvent('on' + h, f);
}
function AddImage(i,t,tl) {
	if(i.complete) {
		t.w = i.width;
		t.h = i.height;
		tl.push(t);
	} else {
		jQuery(i).bind('load',function() {
			t.w = this.width;
			t.h = this.height;
			tl.push(t);
		});
	}
}
function FindWeight(t,a) {
	var w = 1, p;
	if(t.weightFrom) {
		w = 1 * (a.getAttribute(t.weightFrom) || t.textHeight);
	} else if(doc.defaultView && doc.defaultView.getComputedStyle) {
		p = doc.defaultView.getComputedStyle(a,null).getPropertyValue('font-size');
		w = p.replace('px','') * 1;
	} else {
		t.weight = false;
	}
	return w;
}
function MouseMove(e) {
	var i, tc, dd = doc.documentElement, o;
	for(i in TagCanvas.tc) {
		tc = TagCanvas.tc[i];
		o = $(tc.canvas).offset();
		if(e.pageX) {
			tc.mx = e.pageX - o.left;
			tc.my = e.pageY - o.top;
		} else {
			tc.mx = e.clientX + (dd.scrollLeft || doc.body.scrollLeft) - o.left;
			tc.my = e.clientY + (dd.scrollTop || doc.body.scrollTop) - o.top;
		}
	}
}
function MouseClick(e) {
	var t = TagCanvas, cb = doc.addEventListener ? 0 : 1,
		tg = e.target && Defined(e.target.id) ? e.target.id : e.srcElement.parentNode.id;
	if(tg && e.button == cb && t.tc[tg]) {
		MouseMove(e);
		t.tc[tg].Clicked(e);
	}
}
function MouseWheel(e) {
	var t = TagCanvas,
		tg = e.target && Defined(e.target.id) ? e.target.id : e.srcElement.parentNode.id;
	if(tg && t.tc[tg]) {
		e.cancelBubble = true;
		e.returnValue = false;
		e.preventDefault && e.preventDefault();
		t.tc[tg].Wheel((e.wheelDelta || e.detail) > 0);
	}
}
function DrawCanvas() {
	var t = TagCanvas.tc, i;
	for(i in t)
		t[i].Draw();
}
function RotX(p1,t) {
	var s = sin(t), c = cos(t); 
	return {x:p1.x, y:(p1.y * c) + (p1.z * s), z:(p1.y * -s) + (p1.z * c)};
}
function RotY(p1,t) {
	var s = sin(t), c = cos(t); 
	return {x:(p1.x * c) + (p1.z * -s), y:p1.y, z:(p1.x * s) + (p1.z * c)};
}
function Project(tc,p1,w,h,fov,asp) {
	var yn, xn, zn, m = tc.z1 / (tc.z1 + tc.z2 + p1.z);
	yn = p1.y * m;
	xn = p1.x * m;
	zn = tc.z2 + p1.z;
	return {x:xn, y:yn, z:zn};
}
function Outline(tc) {
	this.ts = new Date().valueOf();
	this.tc = tc;
	this.x = this.y = this.w = this.h = this.sc = 1;
	this.z = 0;
}
Oproto = Outline.prototype;
Oproto.Update = function(x,y,w,h,sc,p) {
	var o = this.tc.outlineOffset;
	this.x = sc * (x - o);
	this.y = sc * (y - o);
	this.w = sc * (w + o * 2);
	this.h = sc * (h + o * 2);
	this.sc = sc;
	this.z = p.z;
};
Oproto.Draw = function(c) {
	var diff = new Date().valueOf() - this.ts, t = this.tc;
	c.setTransform(1,0,0,1,0,0);
	c.strokeStyle = t.outlineColour;
	c.lineWidth = t.outlineThickness;
	c.shadowBlur = c.shadowOffsetX = c.shadowOffsetY = 0;
	if(t.pulsateTo < 1)
		c.globalAlpha = t.pulsateTo + ((1 - t.pulsateTo) * 
			(0.5 + (cos(2 * Math.PI * diff / (1000 * t.pulsateTime)) / 2)));
	else
		c.globalAlpha = 1;
	c.strokeRect(this.x, this.y, this.w, this.h);
};
Oproto.Active = function(c,x,y) {
	return (x >= this.x && y >= this.y &&
		x <= this.x + this.w && y <= this.y + this.h);
};
function Tag(tc,name,a,v,w,h) {
	var c = tc.ctxt, i;
	this.tc = tc;
	this.image = name.src ? name : null;
	this.name = name.src ? '' : name;
	this.a = a;
	this.p3d = { x: v[0] * tc.radius * 1.1, y: v[1] * tc.radius * 1.1, z: v[2] * tc.radius * 1.1};
	this.x = this.y = 0;
	this.w = w;
	this.h = h;
	this.colour = tc.textColour;
	this.weight = this.sc = this.alpha = 1;
	this.weighted = !tc.weight;
	this.outline = new Outline(tc);
	if(this.image) {
		if(tc.txtOpt && tc.shadow) {
			i = AddShadowToImage(this.image,tc.shadow,tc.shadowBlur,tc.shadowOffset);
			if(i) {
				this.image = i;
				this.w = i.width;
				this.h = i.height;
			}
		}
	} else {
		this.textHeight = tc.textHeight;
		this.extents = FindTextBoundingBox(this.name, tc.textFont, this.textHeight);
		this.Measure(c,tc);
	}
	this.SetShadowColour = tc.shadowAlpha ? this.SetShadowColourAlpha : this.SetShadowColourFixed;
	this.SetDraw(tc);
}
Tproto = Tag.prototype;
Tproto.SetDraw = function(t) {
	this.Draw = this.image ? (t.ie > 7 ? this.DrawImageIE : this.DrawImage) : this.DrawText;
};
Tproto.Measure = function(c,t) {
	this.h = this.extents ? this.extents.max.y + this.extents.min.y : this.textHeight;
	c.font = this.font = this.textHeight + 'px ' + t.textFont;
	this.w1 = c.measureText(this.name).width;
	if(t.txtOpt) {
		var s = t.txtScale, th = s * this.textHeight, f = th + 'px ' + t.textFont,
			soff = [s*t.shadowOffset[0],s*t.shadowOffset[1]], cw;
		c.font = f;
		cw = c.measureText(this.name).width;
		this.image = TextToCanvas(this.name, f, th, cw, s * this.h, this.colour,
			t.shadow, s * t.shadowBlur, soff);
		if(this.image) {
			this.w = this.image.width / s;
			this.h = this.image.height / s;
		}
		this.SetDraw(t);
		t.txtOpt = this.image;
	}
};
Tproto.SetWeight = function(w) {
	this.weight = w;
	this.Weight(this.tc.ctxt, this.tc);
	this.Measure(this.tc.ctxt, this.tc);
};
Tproto.Weight = function(c,t) {
	var w = this.weight, m = t.weightMode;
	this.weighted = true;
	if(m == 'colour' || m == 'both')
		this.colour = FindGradientColour(t, (w - t.min_weight) / (t.max_weight-t.min_weight));
	if(m == 'size' || m == 'both')
		this.textHeight = w * t.weightSize;
	this.extents = FindTextBoundingBox(this.name, t.textFont, this.textHeight);
};
Tproto.SetShadowColourFixed = function(c,s,a) {
	c.shadowColor = s;
};
Tproto.SetShadowColourAlpha = function(c,s,a) {
	c.shadowColor = SetAlpha(s, a);
};
Tproto.DrawText = function(c,xoff,yoff) {
	var t = this.tc, x = this.x, y = this.y, w, h, s = this.sc, o = this.outline;

	c.globalAlpha = this.alpha;
	c.setTransform(s,0,0,s,0,0);
	c.fillStyle = this.colour;
	t.shadow && this.SetShadowColour(c,t.shadow,this.alpha);
	c.font = this.font;
	w = this.w1 * s;
	h = this.h * s;
	x += 1 + (xoff / s) - (w / 2);
	y += 1 + (yoff / s) - (h / 2);

	c.fillText(this.name, x, y);
	o.Update(x, y, this.w1, this.h, s, this.p3d);
	return o.Active(c, t.mx, t.my) ? o : null;
};
Tproto.DrawImage = function(c,xoff,yoff) {
	var t = this.tc, x = this.x, y = this.y, s = this.sc, o = this.outline, i = this.image, w = this.w, h = this.h;
	c.globalAlpha = this.alpha;
	c.setTransform(s,0,0,s,0,0);
	c.fillStyle = this.colour;
	t.shadow && this.SetShadowColour(c,t.shadow,this.alpha);
	x += (xoff / s) - (w / 2);
	y += (yoff / s) - (h / 2);

	c.drawImage(i, x, y, w, h);
	o.Update(x, y, w, h, s, this.p3d);
	return o.Active(c, t.mx, t.my) ? o : null;
};
Tproto.DrawImageIE = function(c,xoff,yoff) {
	var t = this.tc, i = this.image, s = this.sc, o = this.outline,
		w = i.width = this.w*s, h = i.height = this.h * s,
		x = (this.x*s) + xoff - (w/2), y = (this.y*s) + yoff - (h/2);
	c.globalAlpha = this.alpha;
	c.drawImage(i, x, y);
	o.Update(x, y, w, h, 1, this.p3d);
	return o.Active(c, t.mx, t.my) ? o : null;
};
Tproto.Calc = function(yaw,pitch) {
	var pp = RotY(this.p3d,yaw), t = this.tc, mb = t.minBrightness, r = t.radius;
	this.p3d = RotX(pp,pitch);
	pp = Project(t, this.p3d, this.w, this.h, Math.PI / 4, 20);
	this.x = pp.x;
	this.y = pp.y;
	this.sc = (t.z1 + t.z2 - pp.z) / t.z2;
	this.alpha = Math.max(mb,Math.min(1,mb + 1 - ((pp.z - t.z2 + r) / (2 * r))));
};
Tproto.Clicked = function(e) {
	var a = this.a, t = a.target, h = a.href, evt;
	if(t != '' && t != '_self') {
		if(self.frames[t])
			self.frames[t] = h;
		else if(top.frames[t])
			top.frames[t] = h;
		else
			window.open(h, t);
		return;
	}
	if(a.fireEvent) {
		if(!a.fireEvent('onclick'))
			return;
	} else {
		evt = doc.createEvent('MouseEvents');
		evt.initMouseEvent('click', 1, 1, window, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, null);
		if(!a.dispatchEvent(evt))
			return;
	}
	doc.location = h;
};
function TagCanvas() { 
	var i, opts = {
	mx : -1, my : -1,
	z1 : 20000, z2 : 20000, z0 : 0.0002,
	freezeActive : false,
	pulsateTo : 1,
	pulsateTime : 3,
	reverse : false,
	depth : 0.5,
	maxSpeed : 0.05,
	minSpeed : 0,
	decel : 0.95,
	interval : 20,
	initial : null,
	hideTags: true,
	minBrightness : 0.1,
	outlineColour : '#ffff99',
	outlineThickness : 2,
	outlineOffset : 5,
	textColour : '#ff99ff',
	textHeight : 15,
	textFont : 'Helvetica, Arial, sans-serif',
	shadow: '#000',
	shadowBlur: 0,
	shadowOffset: [0,0],
	zoom: 1,
	weight: false,
	weightMode: 'size',
	weightFrom: null,
	weightSize: 1,
	weightGradient: {0:'#f00', 0.33:'#ff0', 0.66:'#0f0', 1:'#00f'},
	txtOpt: true,
	txtScale: 2,
	frontSelect: false,
	wheelZoom: true,
	zoomMin: 0.3,
	zoomMax: 3,
	zoomStep: 0.05,
	shape: 'sphere',
	lock: null
	};
	for(i in opts)
		this[i] = opts[i];
	this.max_weight = 0;
	this.min_weight = 200;
}
TCproto = TagCanvas.prototype;
TCproto.Draw = function() {
	var cv = this.canvas, cw = cv.width, ch = cv.height, max_sc = 0, yaw = this.yaw, pitch = this.pitch,
		x1 = cw / 2, y1 = ch / 2, c = this.ctxt, active, a, i, tl = this.taglist, l = tl.length;
	c.setTransform(1,0,0,1,0,0);
	this.active = null;
	for(i = 0; i < l; ++i)
		tl[i].Calc(yaw, pitch);
	tl = tl.sort(function(a,b) {return a.sc-b.sc});

	if(!this.txtOpt && this.shadow) {
		c.shadowBlur = this.shadowBlur;
		c.shadowOffsetX = this.shadowOffset[0];
		c.shadowOffsetY = this.shadowOffset[1];
	}
	c.clearRect(0,0,cw,ch);
	for(i = 0; i < l; ++i) {
		a = tl[i].Draw(c, x1, y1);
		if(a && a.sc > max_sc && (!this.frontSelect || a.z <= 0)) {
			active = a;
			active.index = i;
			max_sc = a.sc;
		}
	}
	if(this.freezeActive && active)
		this.yaw = this.pitch = 0;
	else
		this.Animate(cw, ch);
	active && (this.active = active).Draw(c);
};
TCproto.Animate = function(w,h) {
	var tc = this, x = tc.mx, y = tc.my, l = tc.lock, s, ay, ap, r;
	if(x >= 0 && y >= 0 && x < w && y < h)
	{
		s = tc.maxSpeed, r = tc.reverse ? -1 : 1;
		if(l != 'x')
			this.yaw = r * ((s * 2 * x / w) - s);
		if(l != 'y')
			this.pitch = r * -((s * 2 * y / h) - s);
		this.initial = null;
	}
	else if(!tc.initial)
	{
		s = tc.minSpeed, ay = abs(this.yaw), ap = abs(this.pitch);
		if(l != 'x' && ay > s)
			this.yaw = ay > tc.z0 ? tc.yaw * tc.decel : 0;
		if(l != 'y' && ap > s)
			this.pitch = ap > tc.z0 ? tc.pitch * tc.decel : 0;
	}
};
TCproto.Zoom = function(r) {
	this.z2 = this.z1 * (1/r);
};
TCproto.Clicked = function(e) {
	var a = this.active, t = this.taglist;
	try {
		if(a && t[a.index]) 
			t[a.index].Clicked(e);
	} catch(ex) {
	}
};
TCproto.Wheel = function(i) {
	var z = this.zoom + this.zoomStep * (i ? 1 : -1);
	this.zoom = Math.min(this.zoomMax,Math.max(this.zoomMin,z));
	this.Zoom(this.zoom);
};

TagCanvas.tc = {};

jQuery.fn.tagcanvas = function(options,lctr) {
	var links, ctr = lctr ? jQuery('#'+lctr) : this;
	if(doc.all && !lctr) return false; // IE must have external list
	links = ctr.find('a');
	if(Defined(window.G_vmlCanvasManager)) {
		this.each(function() { $(this)[0] = window.G_vmlCanvasManager.initElement($(this)[0]); });
		options.ie = parseFloat(navigator.appVersion.split('MSIE')[1]);
	}

	if(!links.length || !this[0].getContext || !this[0].getContext('2d').fillText)
		return false;

	this.each(function() {
		var i, vl, im, ii, tag, jqt, w, weights = [],
			pfuncs = {
				sphere:PointsOnSphere,
				vcylinder:PointsOnCylinderV,
				hcylinder:PointsOnCylinderH
			};

		// if using internal links, get only the links for this canvas
		lctr || (links = $(this).find('a'));
			
		jqt = new TagCanvas;
		for(i in options)
			jqt[i] = options[i];

		jqt.z1 = (19800 / (Math.exp(jqt.depth) * (1-1/Math.E))) +
			20000 - 19800 / (1-(1/Math.E));
		jqt.z2 = jqt.z1 * (1/jqt.zoom);

		jqt.radius = (this.height > this.width ? this.width : this.height)
			* 0.33 * (jqt.z2 + jqt.z1) / (jqt.z1);
		jqt.yaw = jqt.initial ? jqt.initial[0] * jqt.maxSpeed : 0;
		jqt.pitch = jqt.initial ? jqt.initial[1] * jqt.maxSpeed : 0;
		jqt.canvas = $(this)[0];
		jqt.ctxt = jqt.canvas.getContext('2d');
		jqt.textFont = FixFont(jqt.textFont);
		jqt.ctxt.textBaseline = 'top';
		if(jqt.shadowBlur || jqt.shadowOffset[0] || jqt.shadowOffset[1]) {
			// let the browser translate "red" into "#ff0000"
			jqt.ctxt.shadowColor = jqt.shadow;
			jqt.shadow = jqt.ctxt.shadowColor;
			jqt.shadowAlpha = ShadowAlphaBroken();
		} else {
			delete jqt.shadow;
		}
		jqt.taglist = [];

		jqt.shape = pfuncs[jqt.shape] || pfuncs.sphere;
		vl = jqt.shape(links.length);
		for(i = 0; i < links.length; ++i) {
			im = links[i].getElementsByTagName('img');
			if(im.length) {
				ii = new Image;
				ii.src = im[0].src;
				tag = new Tag(jqt,ii, links[i], vl[i], 1, 1);
				AddImage(ii,tag,jqt.taglist);
			} else {
				jqt.taglist.push(new Tag(jqt,links[i].innerText || links[i].textContent, links[i],
					vl[i], 2, jqt.textHeight + 2));
			}
			if(jqt.weight) {
				w = FindWeight(jqt,links[i]);
				if(w > jqt.max_weight) jqt.max_weight = w;
				if(w < jqt.min_weight) jqt.min_weight = w;
				weights.push(w);
			}
		}
		if(jqt.weight = (jqt.max_weight > jqt.min_weight)) {
			for(i = 0; i < jqt.taglist.length; ++i) {
				jqt.taglist[i].SetWeight(weights[i]);
			}
		}

		TagCanvas.tc[$(this)[0].id] = jqt;
		// for some reason, using bind with mouseup isn't working in IE
		AddHandler('mousemove', MouseMove, this);
		AddHandler('mouseout', MouseMove, this);
		AddHandler('mouseup', MouseClick, this);
		if(jqt.wheelZoom) {
			AddHandler('mousewheel', MouseWheel, this);
			AddHandler('DOMMouseScroll', MouseWheel, this);
		}
		lctr && jqt.hideTags && ctr.hide();
		options.interval = options.interval || jqt.interval;
	});
	return !!(TagCanvas.started || (TagCanvas.started = setInterval(DrawCanvas, options.interval)));
};
})(jQuery);
