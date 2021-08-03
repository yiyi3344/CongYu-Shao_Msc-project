var riaActionCreator = (function() {
	var PI = Math.PI;

	function Creator(w) {
		this.w = w;
		this.init();
	}

	Creator.prototype = {
		init: function() {
			var that = this,
				w = that.w;
			that.width = w.width();
			that.height = w.height();
			w.html('<canvas width="' + that.width + '" height="' + that.height + '"></canvas>');
			that.ctx = $('canvas', w)[0].getContext('2d');
		},
		clearup: function() {
			this.ctx.clearRect(0, 0, this.width, this.height);
			this.ctx.canvas.width = this.width;
			this.ctx.canvas.height = this.height;
			return this;
		},
		setDatas: function(s, f) {
			var that = this,
				i, l, d, type;
			for (i = 0, l = s.length; i < l; i++) {
				d = s[i];
				type = d['type'];
				if (f(d) && typeof that[type] === 'function') {
					that[type].call(that, d);
				}
			}
		},
		getRadius: function(deg) {
			return deg * PI / 180;
		},
		getDeg: function(radius) {
			return radius * 180 / PI;
		},
		setPass: function(s) {
			var that = this,
				ctx = that.ctx,
				sx = s.sy * 3.44 + 8,
				sy = s.sx * 5.14 + 23,
				ex = s.ey * 3.44 + 8,
				ey = s.ex * 5.14 + 23,
				r = Math.atan2(sy - ey, ex - sx),
				t = (sx === ex) ? Math.abs(ey - sy) : (sy === ey) ? Math.abs(sx - ex) : Math.abs((sy - ey) / Math.sin(r));
			ctx.lineWidth = 2;
			ctx.save();
			ctx.translate(ex, ey);
			ctx.rotate(-r);
			ctx.beginPath();
			ctx.moveTo(0, 0);
			ctx.lineTo(-1 * t, 0);
			ctx.stroke();
			ctx.beginPath();
			ctx.moveTo(0, 0);
			ctx.lineTo(-12, -6);
			ctx.lineTo(-8, 0);
			ctx.lineTo(-12, 6);
			ctx.closePath();
			ctx.fill();
			ctx.restore();
		},
		setShoot: function(s) {
			var that = this,
				ctx = that.ctx,
				sx = s.sy * 3.44 + 8,
				sy = s.sx * 5.14 + 23,
				ex = s.ey * 3.44 + 8,
				ey = s.ex * 5.14 + 23,
				r = Math.atan2(sy - ey, ex - sx),
				t = (sx === ex) ? (ey - sy) : (sy === ey) ? (sx - ex) : (sy - ey) / Math.sin(r);
			ctx.lineWidth = 2;
			ctx.save();
			ctx.translate(ex, ey);
			ctx.rotate(-r);
			ctx.beginPath();
			ctx.moveTo(-6, 0);
			ctx.lineTo(-1 * t, 0);
			ctx.stroke();
			ctx.beginPath();
			ctx.moveTo(-12, -6);
			ctx.lineTo(0, 0);
			ctx.lineTo(-12, 6);
			ctx.stroke()
			ctx.restore();
		},
		setContest: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23,
				dit = PI * 4 / 5,
				r = 7,
				sin = Math.sin(0) * r,
				cos = Math.cos(0) * r,
				i, d;
			ctx.lineWidth = 2;
			ctx.save();
			ctx.translate(x, y);
			ctx.rotate(-1 * PI / 2);
			ctx.beginPath();
			ctx.moveTo(cos, sin);
			for (i = 0; i < 5; i++) {
				d = dit * i;
				sin = Math.sin(d) * r;
				cos = Math.cos(d) * r;
				ctx.lineTo(cos, sin);
			}
			ctx.closePath();
			ctx.fill();
			ctx.restore();
		},
		setScrimmage: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 3;
			ctx.beginPath();
			ctx.moveTo(x - 6, y + 5);
			ctx.lineTo(x, y - 5);
			ctx.lineTo(x + 6, y + 5);
			ctx.stroke();
		},
		setFoul: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 1;
			ctx.beginPath();
			ctx.moveTo(x, y - 7);
			ctx.lineTo(x - 6, y + 5);
			ctx.lineTo(x + 6, y + 5);
			ctx.closePath();
			ctx.stroke();
			ctx.fill();
		},
		setSlip: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 1;
			ctx.beginPath();
			ctx.moveTo(x + 5, y - 7);
			ctx.lineTo(x - 4, y - 7);
			ctx.lineTo(x - 9, y);
			ctx.lineTo(x - 4, y + 7);
			ctx.lineTo(x + 5, y + 7);
			ctx.closePath();
			ctx.fill();
		},
		setTackle: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.moveTo(x - 7, y - 7);
			ctx.lineTo(x + 7, y + 7);
			ctx.moveTo(x - 7, y + 7);
			ctx.lineTo(x + 7, y - 7);
			ctx.stroke();
		},
		setIntercept: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 1;
			ctx.beginPath();
			ctx.moveTo(x, y - 7);
			ctx.lineTo(x - 4, y);
			ctx.lineTo(x, y + 7);
			ctx.lineTo(x + 4, y);
			ctx.closePath();
			ctx.fill();
		},
		setBlock: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.moveTo(x, y - 6);
			ctx.lineTo(x, y + 6);
			ctx.moveTo(x - 6, y);
			ctx.lineTo(x + 6, y);
			ctx.stroke();
		},
		setRescue: function(s) {
			return;
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.arc(x, y, 6, 0, PI * 2);
			ctx.stroke();
		},
		setBlockshoot: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 4;
			ctx.beginPath();
			ctx.moveTo(x, y - 6);
			ctx.lineTo(x, y + 6);
			ctx.stroke();
		},
		setBlockpass: function(s) {
			var that = this,
				ctx = that.ctx,
				x = s.y * 3.44 + 8,
				y = s.x * 5.14 + 23;
			ctx.lineWidth = 4;
			ctx.beginPath();
			ctx.moveTo(x - 6, y);
			ctx.lineTo(x + 6, y);
			ctx.stroke();
		},
		'1': function(s) {
			this.ctx.strokeStyle = '#2fc5f3';
			this.ctx.fillStyle = '#2fc5f3';
			this.setPass(s);
		},
		'2': function(s) {
			this.ctx.strokeStyle = '#cc0010';
			this.ctx.fillStyle = '#cc0010';
			this.setPass(s);
		},
		'3': function(s) {
			this.ctx.strokeStyle = '#f5d965';
			this.ctx.fillStyle = '#f5d965';
			this.setPass(s);
		},
		'4': function(s) {
			this.ctx.strokeStyle = '#a9a9a9';
			this.ctx.fillStyle = '#a9a9a9';
			this.setPass(s);
		},
		'5': function(s) {
			this.ctx.strokeStyle = '#2fc5f3';
			this.ctx.fillStyle = '#2fc5f3';
			this.setShoot(s);
		},
		'6': function(s) {
			this.ctx.strokeStyle = '#cc0010';
			this.ctx.fillStyle = '#cc0010';
			this.setShoot(s);
		},
		'7': function(s) {
			this.ctx.strokeStyle = '#f5d965';
			this.ctx.fillStyle = '#f5d965';
			this.setShoot(s);
		},
		'8': function(s) {
			this.ctx.strokeStyle = '#a9a9a9';
			this.ctx.fillStyle = '#a9a9a9';
			this.setShoot(s);
		},
		'101': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#8cc63f';
			this.setContest(s);
		},
		'102': function(s) {
			this.ctx.strokeStyle = '#f87307';
			this.ctx.fillStyle = '#f87307';
			this.setContest(s);
		},
		'103': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#f87307';
			this.setScrimmage(s);
		},
		'104': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#f87307';
			this.setScrimmage(s);
		},
		'105': function(s) {
			this.ctx.strokeStyle = '#070707';
			this.ctx.fillStyle = '#070707';
			this.setFoul(s);
		},
		'106': function(s) {
			this.ctx.strokeStyle = '#e3e3e3';
			this.ctx.fillStyle = '#ffffff';
			this.setFoul(s);
		},
		'107': function(s) {
			this.ctx.strokeStyle = '#e29f00';
			this.ctx.fillStyle = '#e29f00';
			this.setSlip(s);
		},
		'108': function(s) {
			this.ctx.strokeStyle = '#28a8cf';
			this.ctx.fillStyle = '#28a8cf';
			this.setSlip(s);
		},
		'109': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#8cc63f';
			this.setTackle(s);
		},
		'110': function(s) {
			this.ctx.strokeStyle = '#f87307';
			this.ctx.fillStyle = '#f87307';
			this.setTackle(s);
		},
		'111': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#8cc63f';
			this.setRescue(s);
		},
		'112': function(s) {
			this.ctx.strokeStyle = '#f87307';
			this.ctx.fillStyle = '#f87307';
			this.setRescue(s);
		},
		'113': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#8cc63f';
			this.setIntercept(s);
		},
		'114': function(s) {
			this.ctx.strokeStyle = '#8cc63f';
			this.ctx.fillStyle = '#8cc63f';
			this.setBlock(s);
		},
		'115': function(s) {
			this.ctx.strokeStyle = '#a9a9a9';
			this.ctx.fillStyle = '#a9a9a9';
			this.setBlockshoot(s);
		},
		'116': function(s) {
			this.ctx.strokeStyle = '#a9a9a9';
			this.ctx.fillStyle = '#a9a9a9';
			this.setBlockpass(s);
		}
	};
	return {
		create: function(t) {
			return new Creator(t);
		}
	};
})();

var paintAction = function(t, s) {
		var that = this,
			filters = that.actionFilters;
		t.clearup().setDatas(s, function(d) {
			if (!filters) {
				return true;
			}
			return new RegExp('(^|,)' + d.type + '(,|$)').test(filters);
		});
	};