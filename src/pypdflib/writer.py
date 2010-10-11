#!/usr/bin/python
#-*- coding: utf-8 -*-
# pypdflib/writer.py

# pypdflib is a pango/cairo framework for generating reports.
# Copyright © 2010  Santhosh Thottingal <santhosh.thottingal@gmail.com>

# This file is part of pypdflib.
#
# pypdflib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  
#
# pypdflib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pypdflib.  If not, see <http://www.gnu.org/licenses/>.


import cairo
import pango
import pangocairo
class PDFWriter():

    def __init__(self,filename, width, height):

        self.width      = width
        self.height     = height
        surface         = cairo.PDFSurface(filename, self.width, self.height)
        self.context    = cairo.Context(surface)

        self.context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        self.pc         = pangocairo.CairoContext(self.context)
        self.pf_desc    = pango.FontDescription()
        self.position_x = 0
        self.position_y = 0

        self.left_margin        = self.width*0.1
        self.right_margin       = self.width*0.1
        self.top_margin         = self.width*0.1
        self.bottom_margin      = self.width*0.1

        self.line_width         = 10
        self.font_size          = 10
        self.para_break_width   = 5

        self.page_num       = 0
        self.ybottom        = self.height - self.bottom_margin*2
        self.header         = None
        self.footer         = None
        
    def set_header(self, header):
        """
            Sets the header of the page
        """
        self.header = header 
        
    def set_footer(self, footer):
        """
            Sets the footer of the page
        """
        self.footer = footer
        
    def add_h1(self, text):
        '''
                Add heading-1 to document
        '''

        self.assert_page_break()
        h1_font_description = self.pf_desc

        h1_font_description.set_family(text.font)
        h1_font_description.set_size((int)(text.font_size* pango.SCALE))

        h1_layout = pangocairo.CairoContext(self.context).create_layout()
        h1_layout.set_font_description(h1_font_description)
        h1_layout.set_text(str(text.text))

        ink_rect, logical_rect = h1_layout.get_extents()

        ##  COMMENTS ##
        if self.position_y==0:
            self.position_y+=self.top_margin 

        self.position_y +=  self.line_width*1

        self.assert_page_break()
        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h1_layout)

        self.position_y +=  logical_rect[3]/pango.SCALE+self.para_break_width
        
    def add_h2(self, text):
        '''
                Add heading-2 to document
        '''

        h2_font_description = self.pf_desc

        h2_font_description.set_family(text.font)
        h2_font_description.set_size((int)(text.font_size* pango.SCALE))

        h2_layout = pangocairo.CairoContext(self.context).create_layout()
        h2_layout.set_font_description(h2_font_description)
        h2_layout.set_text(str(text.text))

        ink_rect, logical_rect = h2_layout.get_extents()

        ##  COMMENTS ##
        if self.position_y==0:
            self.position_y+=self.top_margin

        self.position_y +=  self.line_width*1

        self.assert_page_break()
        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h2_layout)

        self.position_y +=  logical_rect[3]/pango.SCALE+self.para_break_width
        
    def add_h3(self, text):
        '''
                Add heading-3 to document
        '''

        self.assert_page_break()

        h3_font_description = self.pf_desc

        h3_font_description.set_family(text.font)
        h3_font_description.set_size((int)(text.font_size* pango.SCALE))

        h3_layout = pangocairo.CairoContext(self.context).create_layout()
        h3_layout.set_font_description(h3_font_description)
        h3_layout.set_text(str(text.text))

        ink_rect, logical_rect = h3_layout.get_extents()

        ##  COMMENTS ##
        if self.position_y==0:
            self.position_y+=self.top_margin

        self.position_y +=  self.line_width*1

        self.assert_page_break()

        self.context.move_to(self.left_margin, self.position_y)
        self.pc.show_layout(h3_layout)
        self.position_y +=  logical_rect[3]/pango.SCALE+self.para_break_width
    
    def add_li(self, text):
        '''
                TODO
        '''

        if(text.text==None):return

        self.assert_page_break()

        li_font_description = self.pf_desc

        li_font_description.set_family(text.font)
        li_font_description.set_size((int)(text.font_size* pango.SCALE))

        li_layout = pangocairo.CairoContext(self.context).create_layout()

        li_layout.set_font_description(li_font_description)
        li_layout.set_text(str(text.text))

        ink_rect, logical_rect = li_layout.get_extents()

        ##  COMMENTS ##
        if self.position_y==0:
            self.position_y+=self.top_margin

        self.position_y +=  self.line_width*1
        self.position_x +=  self.left_margin+self.line_width*1

        self.context.move_to(self.position_x, self.position_y)
        self.pc.show_layout(li_layout)

        self.position_y+=logical_rect[3]/pango.SCALE+self.para_break_width
        self.position_x=0
        
    def write_footer(self,footer):

        if footer == None: return 

        footer_font_description = self.pf_desc

        footer_font_description.set_family(footer.font)
        footer_font_description.set_size((int)(footer.font_size* pango.SCALE))

        footer_layout = pangocairo.CairoContext(self.context).create_layout()
        footer_layout.set_font_description(footer_font_description)

        ##  COMMENTS ##
        if footer.markup:
            foote_layout.set_text(str(footer.markup))
        else:
            footer_layout.set_text(str(footer.text))

        ink_rect, logical_rect = footer_layout.get_extents()
        y_position = self.height - self.bottom_margin- logical_rect[3]/pango.SCALE

        self.context.move_to(self.width/2, y_position)
        self.pc.show_layout(footer_layout)
        self.draw_line(y_position)

        self.ybottom = y_position-self.line_width
        
    def write_header(self, header):

        if header == None: return 

        header_font_description = self.pf_desc

        header_font_description.set_family(header.font)
        header_font_description.set_size((int)(header.font_size * pango.SCALE))

        header_layout = pangocairo.CairoContext(self.context).create_layout()

        header_layout.set_font_description(header_font_description)
        header_layout.set_alignment(header.text_align)

        ##  COMMENTS ##
        if header.markup:
            header_layout.set_markup(str(header.markup))
        else:
            header_layout.set_text(str(header.text))

        ink_rect, logical_rect = header_layout.get_extents()

        self.context.move_to(self.left_margin, self.top_margin)
        self.pc.show_layout(header_layout)

        y_position = self.top_margin+(logical_rect[3] / pango.SCALE)
        self.draw_line(y_position)

        self.position_y = y_position + self.line_width
        
    def draw_line(self,y_position):

        self.context.move_to(self.left_margin, y_position)

        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        self.context.line_to(self.width-self.right_margin,  y_position)
        self.context.stroke()

        self.position_y += self.line_width
        
    def add_paragraph(self, paragraph):

        self.position_y += self.para_break_width

        self.position = (self.left_margin, self.position_y)

        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)

        paragraph_layout            = pangocairo.CairoContext(self.context).create_layout()
        paragraph_font_description  = self.pf_desc

        paragraph_font_description.set_family(paragraph.font)
        paragraph_font_description.set_size((int)(paragraph.font_size * pango.SCALE))
        paragraph_layout.set_font_description(paragraph_font_description)

        paragraph_layout.set_width((int)((self.width - self.left_margin-self.right_margin) * pango.SCALE))

        ##  COMMENTS ##
        if(paragraph.justify):
            paragraph_layout.set_justify(True)

        paragraph_layout.set_text(paragraph.text+"\n")#fix it , adding new line to keep the looping correct?!

        self.context.move_to(*self.position)

        pango_layout_iter   = paragraph_layout.get_iter();
        itr_has_next_line   = True

        ##  COMMENTS ##
        while not pango_layout_iter.at_last_line():

            first_line = True
            self.context.move_to(self.left_margin, self.position_y)

            ##  COMMENTS ##
            while not pango_layout_iter.at_last_line() :

                ink_rect, logical_rect  = pango_layout_iter.get_line_extents()
                line                    = pango_layout_iter.get_line_readonly()
                has_next_line           = pango_layout_iter.next_line()

                # Decrease paragraph spacing
                if  ink_rect[2] == 0 : #It is para break

                    dy = self.font_size / 2
                    self.position_y += dy

                    ##  COMMENTS ##
                    if not first_line:

                        self.context.rel_move_to(0, dy)

                else:

                    xstart = 1.0 * logical_rect[0] / pango.SCALE

                    self.context.rel_move_to(xstart, 0)
                    self.pc.show_layout_line( line)

                    line_height = (int)(logical_rect[3] / pango.SCALE)

                    self.context.rel_move_to(-xstart, line_height )
                    self.position_y += line_height 
 
                ##  COMMENTS ##
                if self.position_y > self.ybottom:

                    self.page_num= self.page_num+1
                    self.write_header(self.header)

                    if self.footer:
                        self.footer.set_text(str(self.page_num))
                        self.write_footer(self.footer)

                    self.context.show_page()
                    
                    break
                    
            first_line = False

    def flush(self) :   

        self.page_num= self.page_num+1
        self.write_header(self.header)
        self.footer.set_text(str(self.page_num))
        self.write_footer(self.footer)
        self.context.show_page()
    
    def draw_table(self, table):

        if table.row_count == 0: 
            print("Table has no rows")
            return 

        self.context.identity_matrix()
        self.context.set_source_rgba (0.0, 0.0, 0.0, 1.0)

        x1 = self.left_margin
        y1 = self.top_margin

        width=height=0

        ## COMMENTS ##
        for row in range(table.row_count):

            ## COMMENTS ##
            for column in range(table.column_count):

                height = table.rows[row].height
                width  = table.rows[row].cells[column].width    

                self.context.set_line_width(table.border_width)
                self.context.rectangle(x1,y1,width,height)
                self.context.stroke()
                self.draw_cell(table.rows[row].cells[column],x1,y1,x1+width,y1+height)
                x1 += width

            y1+=height    
            x1= self.left_margin   
            self.position_y+=height
                
    def draw_cell(self, cell, x1, y1, x2, y2):

        cell_font_description = self.pf_desc

        cell_font_description.set_family(cell.font)
        cell_font_description.set_size((int)(cell.font_size* pango.SCALE))

        cell_layout = pangocairo.CairoContext(self.context).create_layout()

        cell_layout.set_width(int(x2-x1)*pango.SCALE)
        cell_layout.set_justify(True)
        cell_layout.set_font_description(cell_font_description)
        cell_layout.set_text(str(cell.text))

        ink_rect, logical_rect = cell_layout.get_extents()

        self.context.move_to(x1,y1)
        self.pc.show_layout(cell_layout)
                
    def add_image(self, image):

        self.context.save ()
        self.context.move_to(self.left_margin, self.position_y)

        image_surface = cairo.ImageSurface.create_from_png (image.image_file)

        w       = image_surface.get_width ()
        h       = image_surface.get_height ()
        data    = image_surface.get_data()
        stride  = cairo.ImageSurface.format_stride_for_width (cairo.FORMAT_ARGB32, w)

        image_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, w, h,stride)

        self.context.scale(0.5, 0.5)
        self.context.set_source_surface (image_surface,self.left_margin/0.5, self.position_y/0.5)
        self.context.paint()
        self.context.restore ()

        self.position_y+= h*0.5+ image.padding_bottom
        
        
    def new_page(self):

        self.context.identity_matrix()
        self.context.set_source_rgba (1.0, 1.0, 1.0, 1.0)
        self.context.rectangle(0, self.position_y, self.width, self.height)
        self.context.fill()
        self.context.set_source_rgb (0.0, 0.0, 0.0)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=0    
        self.context.show_page()
        
    def blank_space(self, height):

        self.context.identity_matrix()
        self.context.set_source_rgba (1.0, 1.0, 1.0, 1.0)
        self.context.rectangle(0, self.position_y, self.width, height)
        self.context.fill()
        self.context.set_source_rgb (0.0, 0.0, 0.0)
        self.context.move_to(self.left_margin, self.top_margin)
        self.position_y=0    
        
                    
    def page_break(self):

        self.page_num= self.page_num+1
        self.write_header(self.header)

        if self.footer:
            self.footer.set_text(str(self.page_num))
            self.write_footer(self.footer)

        self.context.show_page()
        
    def assert_page_break(self):

        if  self.position_y > self.ybottom:
            self.page_break()

