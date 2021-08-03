function radar(data) {
	var option = {
		tooltip: {
			trigger: 'item'
		},
		radar: {
			name: {
				textStyle: {
					color: 'black',
					backgroundColor: 'yellow',
					borderRadius: 3,
					padding: [3, 5]
				}
			},
			indicator: [{
				name: 'TotalPasses',
				max: 400
			}, {
				name: 'AccSP',
				max: 400
			}, {
				name: 'TotalTackles',
				max: 20
			}, {
				name: 'Interception',
				max: 20
			}, {
				name: 'AccLB',
				max: 30
			}]
		},
		series: [{
			name: 'data',
			type: 'radar',
			areaStyle: {
				normal: {}
			},
			data: data
		}]
	};
	return option
}