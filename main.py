#import curses
from pitch_sheet import PitchSheet

#add menu here later
def main():
    low_pitch = 74.0
    high_pitch = 76.0
    page_dimensions = (8.5, 11.0)
    page_dpi = (360, 360)
    ps = PitchSheet(low_pitch, high_pitch, page_dimensions, page_dpi)
    ps.generate_pitch_sheet()

if __name__ == "__main__":
    main()