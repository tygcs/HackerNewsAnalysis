$(function(){
			var data = [
			        	{name : 'Android',value : 52.5,color:'#4572a7'},
			        	{name : 'IOS',value : 34.3,color:'#aa4643'},
			        	{name : 'RIM',value : 8.4,color:'#89a54e'},
			        	{name : 'Microsoft',value : 3.6,color:'#80699b'},
			        	{name : 'Other',value : 1.2,color:'#3d96ae'}
		        	];

	    	
			var chart = new iChart.Pie3D({
				render : 'canvasDiv',
				data: data,
				title : {
					text : 'Mobile-Friendly Distribution',
					height:40,
					fontsize : 30,
					color : '#282828'
				},
				footnote : {
					text : 'ichartjs.com',
					color : '#486c8f',
					fontsize : 12,
					padding : '0 38'
				},
				sub_option : {
					mini_label_threshold_angle : 40,//����label�ķ�ֵ,��λ:�Ƕ�
					mini_label:{//����label������
						fontsize:20,
						fontweight:600,
						color : '#ffffff'
					},
					label : {
						background_color:null,
						sign:false,//���ý���label��Сͼ��
						padding:'0 4',
						border:{
							enable:false,
							color:'#666666'
						},
						fontsize:11,
						fontweight:600,
						color : '#4572a7'
					},
					border : {
						width : 2,
						color : '#ffffff'
					},
					listeners:{
						parseText:function(d, t){
							return d.get('value')+"%";//�Զ���label�ı�
						}
					} 
				},
				legend:{
					enable:true,
					padding:0,
					offsetx:120,
					offsety:50,
					color:'#3e576f',
					fontsize:20,//�ı���С
					sign_size:20,//Сͼ���С
					line_height:28,//�����и�
					sign_space:10,//Сͼ�����ı����
					border:false,
					align:'left',
					background_color : null//͸������
				},
				animation : true,//�������ɶ���
				animation_duration:800,//800ms��ɶ��� 
				shadow : true,
				shadow_blur : 6,
				shadow_color : '#aaaaaa',
				shadow_offsetx : 0,
				shadow_offsety : 0,
				background_color:'#f1f1f1',
				align:'right',//�Ҷ���
				offsetx:-100,//������x�Ḻ����ƫ��λ��60px
				offset_angle:-90,//��ʱ��ƫ��120��
				width : 800,
				height : 400,
				radius:150
			});
			//�����Զ�����������Ҳ�˵���ı�
			chart.plugin(new iChart.Custom({
					drawFn:function(){
						//���Ҳ��λ�ã���Ⱦ˵������
						chart.target.textAlign('start')
						.textBaseline('top')
						.textFont('600 20px Verdana')
						.fillText('Market Fragmentation:\nTop Mobile\nOperating Systems',120,80,false,'#be5985',false,24)
						.textFont('600 12px Verdana')
						.fillText('Source:ComScore,2012',120,160,false,'#999999');
					}
			}));
			
			chart.draw();
		});// JavaScript Document