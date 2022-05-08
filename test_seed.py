from models import User, Submitted_Data
from app import app, db



u1 = User.register(username='habibi69', pwd = '123')
u2 = User.register(username='george', pwd = '123')
u3 = User.register(username='steve', pwd = '123')
u4 = User.register(username='jones', pwd = '123')
u5 = User.register(username='harper', pwd = '123')
u6 = User.register(username='marty', pwd = '123')
u7 = User.register(username='tezy', pwd = '123')

sd1 = Submitted_Data(stopNo = 1, busNo = 15, delay=16, user_id=1, noShow=False, date_submitted='2022-04-28 03:02:37.433533')
sd2 = Submitted_Data(stopNo = 131, busNo = 15, noShow=True, user_id=2, date_submitted='2022-04-28 03:02:37.433533')
sd3 = Submitted_Data(stopNo = 12, busNo = 43, noShow=True, date_submitted='2022-04-26 03:02:37.433533')
sd4 = Submitted_Data(stopNo = 77, busNo = 55, delay=10, noShow=False,  date_submitted='2022-04-23 03:02:37.433533')

db.session.add_all([u1,u2,u3,u4,u5,u6,u7,sd1,sd2,sd3,sd4])
db.session.commit()



