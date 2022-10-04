import streamlit as st
from pyecharts.faker import Faker

from sql_execute import plants_tb_select,farmers_tb_select,dashboard_select,plan_year_options_select,\
sql_independent_variable_details_by_crop_argument,columns_name_independent_weather,weight_year_by_vil,\
columns_name_independent_crop,farm_analysis_select
from calculate import *
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Line
from streamlit_echarts import st_pyecharts, st_echarts

st.set_page_config(
    page_title="หน้าแรก",
    page_icon="🏠",
    layout="wide"
)

def main():
    st.subheader("หน้าแรก")
    with st.container():
        col1,col2,col3,col4 = st.columns([2,1,1,1])
        with col4:
            plant_options = plants_tb_select()
            plant_options.insert(0,[0,'ทั้งหมด'])
            plant_selected = st.selectbox("พืช",options=plant_options,format_func=lambda plant_options:"{}".format(plant_options[1]))
        # st.write(plant_selected[0])
        dt = dashboard_select(plant_selected[0],'ทั้งหมด')
        columns_independent_weather = columns_name_independent_weather()
        columns_independent_crop = columns_name_independent_crop()
        columns_name = columns_name_for_dataframe(columns_independent_weather, columns_independent_crop)
        df = pd.DataFrame(dt,columns=columns_name)
        # st.write(df)
        dt_group_plant = dashboard_select(plant_selected[0],str('ทั้งหมด'))
        df_group_plant = pd.DataFrame(dt_group_plant,columns=columns_name)
        weight_year_df = df_group_plant[['ปริมาณผลผลิตก่อนตัดแต่ง','plan_year']]
        weight_year_df = weight_year_df.groupby(['plan_year']).sum()
        weight_year_df.reset_index(inplace=True)
        weight_year_df.plan_year = weight_year_df.plan_year.astype(str)
        year_list = weight_year_df['plan_year'].values.tolist()
        weight_list = weight_year_df['ปริมาณผลผลิตก่อนตัดแต่ง'].values.tolist()

    with st.container():
        st.markdown("#### แนวโน้มปริมาณผลผลิตของพืชแต่ละชนิด (กิโลกรัม)")
        weight_trend_plant = (
            Line()
                .add_xaxis(year_list)
                .add_yaxis("ปริมาณผลผลิต", weight_list)
            # .set_global_opts(title_opts=opts.TitleOpts(title="แนวโน้มปริมาณผลผลิต (กิโลกรัม)",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
        )
        st_pyecharts(weight_trend_plant, height="500px",key="weight_trend_plant")
    with st.container():
        col1,col2,col3,col4 = st.columns([2,1,1,1])
        with col4:
            farm_vil_name_options = farm_analysis_select(0)
            farm_vil_selected = st.selectbox("เลือกหมู่บ้าน", options=farm_vil_name_options,
                                             format_func=lambda farm_vil_name_options: "{}".format(
                                                 farm_vil_name_options[0]))
    with st.container():
        col1,col2 = st.columns([1.5,1])
        with col2:
            weight_year_by_vil_dt = weight_year_by_vil(farm_vil_selected[0], plant_selected[0])
            weight_year_by_vil_df = pd.DataFrame(weight_year_by_vil_dt,
                                                 columns=['plan_year', 'plant_weight_before_trim'])
            # weight_group_by_vil_year = weight_year_by_vil_df.groupby(['plan_year']).sum()
            plan_year_df = weight_year_by_vil_df.plan_year.astype(str)
            plan_year_list = plan_year_df.unique().tolist()
            weight_vil_list = weight_year_by_vil_df['plant_weight_before_trim'].values.tolist()
            st.markdown("##### แนวโน้มปริมาณผลผลิต (กิโลกรัม)")
            weight_trend_vil = (
                Line()
                    .add_xaxis(plan_year_list)
                    .add_yaxis("ปริมาณผลผลิต", weight_vil_list)
                    # .set_global_opts(title_opts=opts.TitleOpts(title="แนวโน้มปริมาณผลผลิต (กิโลกรัม)",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
            )
            st_pyecharts(weight_trend_vil,height="500px",key="weight_trend_vil")
        with col1:
            st.markdown("##### สัดส่วนการตรวจคุณภาพแปลงแต่ละหมู่บ้าน (แห่ง)")
            farm_analysis_dt = farm_analysis_select(farm_vil_selected[0])
            farm_analysis_df = pd.DataFrame(farm_analysis_dt,columns=['farm_vil_name','soil_analysis','water_analysis','gap_analysis'])
            farm_analysis_df = farm_analysis_df.rename(columns={'farm_vil_name':'vilname','soil_analysis':'Soil Analysis','water_analysis':'Water Analysis','gap_analysis':'GAP Analysis'})
            farm_analysis_df = farm_analysis_df.transpose()
            farm_analysis_df = farm_analysis_df.drop(farm_analysis_df.index[:1])
            farm_analysis_df = farm_analysis_df.reset_index()
            farm_analysis_df = farm_analysis_df.rename(columns={"index": "name", 0:"value"})
            ls = farm_analysis_df.values.tolist()
            farm_test_vil = (
                Pie()
                    .add("", ls)
                    # .set_global_opts(title_opts=opts.TitleOpts(title="สัดส่วนที่อยู่แปลง",title_textstyle_opts=opts.TextStyleOpts(color="#6e7079",font_size=20)))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            st_pyecharts(farm_test_vil,height="500px",key="farm_test_vil")
    with st.container():
        data = [
                {
                    name: 'Flora',
                    itemStyle: {
                        color: '#da0d68'
                    },
                    children: [
                        {
                            name: 'Black Tea',
                            value: 1,
                            itemStyle: {
                                color: '#975e6d'
                            }
                        },
                        {
                            name: 'Floral',
                            itemStyle: {
                                color: '#e0719c'
                            },
                            children: [
                                {
                                    name: 'Chamomile',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f99e1c'
                                    }
                                },
                                {
                                    name: 'Rose',
                                    value: 1,
                                    itemStyle: {
                                        color: '#ef5a78'
                                    }
                                },
                                {
                                    name: 'Jasmine',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f7f1bd'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Fruity',
                    itemStyle: {
                        color: '#da1d23'
                    },
                    children: [
                        {
                            name: 'Berry',
                            itemStyle: {
                                color: '#dd4c51'
                            },
                            children: [
                                {
                                    name: 'Blackberry',
                                    value: 1,
                                    itemStyle: {
                                        color: '#3e0317'
                                    }
                                },
                                {
                                    name: 'Raspberry',
                                    value: 1,
                                    itemStyle: {
                                        color: '#e62969'
                                    }
                                },
                                {
                                    name: 'Blueberry',
                                    value: 1,
                                    itemStyle: {
                                        color: '#6569b0'
                                    }
                                },
                                {
                                    name: 'Strawberry',
                                    value: 1,
                                    itemStyle: {
                                        color: '#ef2d36'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Dried Fruit',
                            itemStyle: {
                                color: '#c94a44'
                            },
                            children: [
                                {
                                    name: 'Raisin',
                                    value: 1,
                                    itemStyle: {
                                        color: '#b53b54'
                                    }
                                },
                                {
                                    name: 'Prune',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a5446f'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Other Fruit',
                            itemStyle: {
                                color: '#dd4c51'
                            },
                            children: [
                                {
                                    name: 'Coconut',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f2684b'
                                    }
                                },
                                {
                                    name: 'Cherry',
                                    value: 1,
                                    itemStyle: {
                                        color: '#e73451'
                                    }
                                },
                                {
                                    name: 'Pomegranate',
                                    value: 1,
                                    itemStyle: {
                                        color: '#e65656'
                                    }
                                },
                                {
                                    name: 'Pineapple',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f89a1c'
                                    }
                                },
                                {
                                    name: 'Grape',
                                    value: 1,
                                    itemStyle: {
                                        color: '#aeb92c'
                                    }
                                },
                                {
                                    name: 'Apple',
                                    value: 1,
                                    itemStyle: {
                                        color: '#4eb849'
                                    }
                                },
                                {
                                    name: 'Peach',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f68a5c'
                                    }
                                },
                                {
                                    name: 'Pear',
                                    value: 1,
                                    itemStyle: {
                                        color: '#baa635'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Citrus Fruit',
                            itemStyle: {
                                color: '#f7a128'
                            },
                            children: [
                                {
                                    name: 'Grapefruit',
                                    value: 1,
                                    itemStyle: {
                                        color: '#f26355'
                                    }
                                },
                                {
                                    name: 'Orange',
                                    value: 1,
                                    itemStyle: {
                                        color: '#e2631e'
                                    }
                                },
                                {
                                    name: 'Lemon',
                                    value: 1,
                                    itemStyle: {
                                        color: '#fde404'
                                    }
                                },
                                {
                                    name: 'Lime',
                                    value: 1,
                                    itemStyle: {
                                        color: '#7eb138'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Sour/\nFermented',
                    itemStyle: {
                        color: '#ebb40f'
                    },
                    children: [
                        {
                            name: 'Sour',
                            itemStyle: {
                                color: '#e1c315'
                            },
                            children: [
                                {
                                    name: 'Sour Aromatics',
                                    value: 1,
                                    itemStyle: {
                                        color: '#9ea718'
                                    }
                                },
                                {
                                    name: 'Acetic Acid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#94a76f'
                                    }
                                },
                                {
                                    name: 'Butyric Acid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#d0b24f'
                                    }
                                },
                                {
                                    name: 'Isovaleric Acid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#8eb646'
                                    }
                                },
                                {
                                    name: 'Citric Acid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#faef07'
                                    }
                                },
                                {
                                    name: 'Malic Acid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#c1ba07'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Alcohol/\nFremented',
                            itemStyle: {
                                color: '#b09733'
                            },
                            children: [
                                {
                                    name: 'Winey',
                                    value: 1,
                                    itemStyle: {
                                        color: '#8f1c53'
                                    }
                                },
                                {
                                    name: 'Whiskey',
                                    value: 1,
                                    itemStyle: {
                                        color: '#b34039'
                                    }
                                },
                                {
                                    name: 'Fremented',
                                    value: 1,
                                    itemStyle: {
                                        color: '#ba9232'
                                    }
                                },
                                {
                                    name: 'Overripe',
                                    value: 1,
                                    itemStyle: {
                                        color: '#8b6439'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Green/\nVegetative',
                    itemStyle: {
                        color: '#187a2f'
                    },
                    children: [
                        {
                            name: 'Olive Oil',
                            value: 1,
                            itemStyle: {
                                color: '#a2b029'
                            }
                        },
                        {
                            name: 'Raw',
                            value: 1,
                            itemStyle: {
                                color: '#718933'
                            }
                        },
                        {
                            name: 'Green/\nVegetative',
                            itemStyle: {
                                color: '#3aa255'
                            },
                            children: [
                                {
                                    name: 'Under-ripe',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a2bb2b'
                                    }
                                },
                                {
                                    name: 'Peapod',
                                    value: 1,
                                    itemStyle: {
                                        color: '#62aa3c'
                                    }
                                },
                                {
                                    name: 'Fresh',
                                    value: 1,
                                    itemStyle: {
                                        color: '#03a653'
                                    }
                                },
                                {
                                    name: 'Dark Green',
                                    value: 1,
                                    itemStyle: {
                                        color: '#038549'
                                    }
                                },
                                {
                                    name: 'Vegetative',
                                    value: 1,
                                    itemStyle: {
                                        color: '#28b44b'
                                    }
                                },
                                {
                                    name: 'Hay-like',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a3a830'
                                    }
                                },
                                {
                                    name: 'Herb-like',
                                    value: 1,
                                    itemStyle: {
                                        color: '#7ac141'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Beany',
                            value: 1,
                            itemStyle: {
                                color: '#5e9a80'
                            }
                        }
                    ]
                },
                {
                    name: 'Other',
                    itemStyle: {
                        color: '#0aa3b5'
                    },
                    children: [
                        {
                            name: 'Papery/Musty',
                            itemStyle: {
                                color: '#9db2b7'
                            },
                            children: [
                                {
                                    name: 'Stale',
                                    value: 1,
                                    itemStyle: {
                                        color: '#8b8c90'
                                    }
                                },
                                {
                                    name: 'Cardboard',
                                    value: 1,
                                    itemStyle: {
                                        color: '#beb276'
                                    }
                                },
                                {
                                    name: 'Papery',
                                    value: 1,
                                    itemStyle: {
                                        color: '#fefef4'
                                    }
                                },
                                {
                                    name: 'Woody',
                                    value: 1,
                                    itemStyle: {
                                        color: '#744e03'
                                    }
                                },
                                {
                                    name: 'Moldy/Damp',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a3a36f'
                                    }
                                },
                                {
                                    name: 'Musty/Dusty',
                                    value: 1,
                                    itemStyle: {
                                        color: '#c9b583'
                                    }
                                },
                                {
                                    name: 'Musty/Earthy',
                                    value: 1,
                                    itemStyle: {
                                        color: '#978847'
                                    }
                                },
                                {
                                    name: 'Animalic',
                                    value: 1,
                                    itemStyle: {
                                        color: '#9d977f'
                                    }
                                },
                                {
                                    name: 'Meaty Brothy',
                                    value: 1,
                                    itemStyle: {
                                        color: '#cc7b6a'
                                    }
                                },
                                {
                                    name: 'Phenolic',
                                    value: 1,
                                    itemStyle: {
                                        color: '#db646a'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Chemical',
                            itemStyle: {
                                color: '#76c0cb'
                            },
                            children: [
                                {
                                    name: 'Bitter',
                                    value: 1,
                                    itemStyle: {
                                        color: '#80a89d'
                                    }
                                },
                                {
                                    name: 'Salty',
                                    value: 1,
                                    itemStyle: {
                                        color: '#def2fd'
                                    }
                                },
                                {
                                    name: 'Medicinal',
                                    value: 1,
                                    itemStyle: {
                                        color: '#7a9bae'
                                    }
                                },
                                {
                                    name: 'Petroleum',
                                    value: 1,
                                    itemStyle: {
                                        color: '#039fb8'
                                    }
                                },
                                {
                                    name: 'Skunky',
                                    value: 1,
                                    itemStyle: {
                                        color: '#5e777b'
                                    }
                                },
                                {
                                    name: 'Rubber',
                                    value: 1,
                                    itemStyle: {
                                        color: '#120c0c'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Roasted',
                    itemStyle: {
                        color: '#c94930'
                    },
                    children: [
                        {
                            name: 'Pipe Tobacco',
                            value: 1,
                            itemStyle: {
                                color: '#caa465'
                            }
                        },
                        {
                            name: 'Tobacco',
                            value: 1,
                            itemStyle: {
                                color: '#dfbd7e'
                            }
                        },
                        {
                            name: 'Burnt',
                            itemStyle: {
                                color: '#be8663'
                            },
                            children: [
                                {
                                    name: 'Acrid',
                                    value: 1,
                                    itemStyle: {
                                        color: '#b9a449'
                                    }
                                },
                                {
                                    name: 'Ashy',
                                    value: 1,
                                    itemStyle: {
                                        color: '#899893'
                                    }
                                },
                                {
                                    name: 'Smoky',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a1743b'
                                    }
                                },
                                {
                                    name: 'Brown, Roast',
                                    value: 1,
                                    itemStyle: {
                                        color: '#894810'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Cereal',
                            itemStyle: {
                                color: '#ddaf61'
                            },
                            children: [
                                {
                                    name: 'Grain',
                                    value: 1,
                                    itemStyle: {
                                        color: '#b7906f'
                                    }
                                },
                                {
                                    name: 'Malt',
                                    value: 1,
                                    itemStyle: {
                                        color: '#eb9d5f'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Spices',
                    itemStyle: {
                        color: '#ad213e'
                    },
                    children: [
                        {
                            name: 'Pungent',
                            value: 1,
                            itemStyle: {
                                color: '#794752'
                            }
                        },
                        {
                            name: 'Pepper',
                            value: 1,
                            itemStyle: {
                                color: '#cc3d41'
                            }
                        },
                        {
                            name: 'Brown Spice',
                            itemStyle: {
                                color: '#b14d57'
                            },
                            children: [
                                {
                                    name: 'Anise',
                                    value: 1,
                                    itemStyle: {
                                        color: '#c78936'
                                    }
                                },
                                {
                                    name: 'Nutmeg',
                                    value: 1,
                                    itemStyle: {
                                        color: '#8c292c'
                                    }
                                },
                                {
                                    name: 'Cinnamon',
                                    value: 1,
                                    itemStyle: {
                                        color: '#e5762e'
                                    }
                                },
                                {
                                    name: 'Clove',
                                    value: 1,
                                    itemStyle: {
                                        color: '#a16c5a'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Nutty/\nCocoa',
                    itemStyle: {
                        color: '#a87b64'
                    },
                    children: [
                        {
                            name: 'Nutty',
                            itemStyle: {
                                color: '#c78869'
                            },
                            children: [
                                {
                                    name: 'Peanuts',
                                    value: 1,
                                    itemStyle: {
                                        color: '#d4ad12'
                                    }
                                },
                                {
                                    name: 'Hazelnut',
                                    value: 1,
                                    itemStyle: {
                                        color: '#9d5433'
                                    }
                                },
                                {
                                    name: 'Almond',
                                    value: 1,
                                    itemStyle: {
                                        color: '#c89f83'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Cocoa',
                            itemStyle: {
                                color: '#bb764c'
                            },
                            children: [
                                {
                                    name: 'Chocolate',
                                    value: 1,
                                    itemStyle: {
                                        color: '#692a19'
                                    }
                                },
                                {
                                    name: 'Dark Chocolate',
                                    value: 1,
                                    itemStyle: {
                                        color: '#470604'
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    name: 'Sweet',
                    itemStyle: {
                        color: '#e65832'
                    },
                    children: [
                        {
                            name: 'Brown Sugar',
                            itemStyle: {
                                color: '#d45a59'
                            },
                            children: [
                                {
                                    name: 'Molasses',
                                    value: 1,
                                    itemStyle: {
                                        color: '#310d0f'
                                    }
                                },
                                {
                                    name: 'Maple Syrup',
                                    value: 1,
                                    itemStyle: {
                                        color: '#ae341f'
                                    }
                                },
                                {
                                    name: 'Caramelized',
                                    value: 1,
                                    itemStyle: {
                                        color: '#d78823'
                                    }
                                },
                                {
                                    name: 'Honey',
                                    value: 1,
                                    itemStyle: {
                                        color: '#da5c1f'
                                    }
                                }
                            ]
                        },
                        {
                            name: 'Vanilla',
                            value: 1,
                            itemStyle: {
                                color: '#f89a80'
                            }
                        },
                        {
                            name: 'Vanillin',
                            value: 1,
                            itemStyle: {
                                color: '#f37674'
                            }
                        },
                        {
                            name: 'Overall Sweet',
                            value: 1,
                            itemStyle: {
                                color: '#e75b68'
                            }
                        },
                        {
                            name: 'Sweet Aromatics',
                            value: 1,
                            itemStyle: {
                                color: '#d0545f'
                            }
                        }
                    ]
                }
            ]
main()