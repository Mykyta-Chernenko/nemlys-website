when copy from Amika

1) replace only the body of the blog_template.html
2) find blocks like <div class="auto-layout-vertical-K27t5F auto-layout-vertical">
                            <div class="auto-layout-vertical-moxYH4 auto-layout-vertical">
                                <div class="paragraph_1_title-EOgRZe epilogue-medium-black-rock-46px">
                                    $PARAGRAPH_1_TITLE
                                </div>
                                <div class="paragraph_1_description-EOgRZe epilogue-medium-black-rock-20px">
                                    $PARAGRAPH_1_DESCRIPTION
                                </div>
                            </div>
                        </div> in 3 breakpoints and put them into generate_html_page
3) locate the new clas for $INTRO and replace it in the generate_html_page.py