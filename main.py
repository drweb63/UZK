from flask import Flask
from flask import render_template, url_for, redirect, request, flash
from auth import requires_auth, requires_manager, requires_boss, requires_admin
from database import session
from sqlalchemy import desc, update, func
from settings import path_barcode
import random, datetime
from models import (
    Orders,
    Customers,
    Barcode,
    Cartridges,
    Category,
    Tow,
    Close_orders,
    Users,
    Archive_orders,
    Logs
)

app = Flask(__name__)

app.secret_key = '8w9q8DOSHACXNASFZXV'


@app.route('/', methods=['GET','POST'])
@requires_auth
def orders(rows=None,cartridges=None,customers=None,tows=None,full=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%Y-%m-%d")
    cartridges = Cartridges.query.order_by(Cartridges.name).all()
    customers = Customers.query.order_by(Customers.name).all()
    tows = Tow.query.all()
    user = Users.query.filter_by(vision='1').order_by(desc(Users.id)).all()

    full = session.query(Orders.id, Cartridges.name, Customers.name, Tow.fullname, Orders.barcode, Orders.mark, Orders.date)\
        .order_by(desc(Orders.id))\
        .join(Cartridges, Orders.cartridge == Cartridges.id)\
        .join(Customers, Orders.customer == Customers.id)\
        .join(Tow, Orders.tow == Tow.id)

    tmp_orders = {}
    for  order in full:
        if order.name not in tmp_orders:
             tmp_orders[order.name] = []
        tmp_orders[order.name].append(order)

    if request.method == 'POST':
        if request.form['action'] == 'Add':
            if request.form['barcode']:
                barcod = request.form['barcode']
                orderss = Orders.query.filter_by(barcode=barcod).count()
                if orderss != 0:
                    barcodd = request.form['barcode']
                    full = session.query(Orders.id, Cartridges.name, Customers.name, Tow.fullname, Orders.barcode,
                                     Orders.mark, Orders.date)\
                                    .filter_by(barcode=barcodd).join(Cartridges, Orders.cartridge == Cartridges.id)\
                                    .join(Customers, Orders.customer == Customers.id).join(Tow, Orders.tow == Tow.id)

                    tmps_orders = {}
                    for order in full:
                        if order.name not in tmps_orders:
                            tmps_orders[order.name] = []
                        tmps_orders[order.name].append(order)
                    return render_template('orders.html', tows=tows, full=tmps_orders, user=user)
                else:
                    barcode = Barcode.query.filter_by(barcode=barcod).count()
                    if  barcode == 0:
                        flash ('Штрих-код не найден')
                    else:
                        barcode = session.query(Barcode).filter_by(barcode=barcod).first()
                        cartridge = barcode.cartridge
                        customer = barcode.customer
                        mark = request.form['mark']
                        tow = request.form['tow']
                        barcod = barcode.barcode
                        order = Orders(cartridge=cartridge,customer=customer,tow=tow,barcode=barcod,mark=mark,date=date_today)
                        session.add(order)
                        logs = Logs(user=namesd, time=date_today, message='Добавлен заказ. Штрихкод: '+barcod)
                        session.add(logs)
                        session.commit()
                        session.flush()
                        flash ('Заказ успешно добавлен')
                        return redirect(url_for('orders'))
            else:
                return render_template('orders_add.html',cartridges=cartridges,customers=customers,tows=tows, date=date_today, fullnames = namesd)

        if request.form['action'] == 'Full':
            return render_template('full_orders.html')
        if request.form['action'] == 'Chancel':
            return redirect(url_for('orders'))

        if request.form['action'] == 'cst_ord_add':
            cst = request.form['cst_ord']
            customerr = Customers.query.filter_by(name=cst).first()
            return render_template('orders_add_cust.html',cartridges=cartridges,customerr=customerr,tows=tows, date=date_today, fullnames = namesd)

        if request.form['action'] == 'Adds':
            if not request.form['barcode']:
                barcod = random.randint(10000000, 99999999 )
                barcod = str(barcod)
                barcode = Barcode.query.filter_by(barcode=barcod).count()
                while  barcode != 0:
                    barcod = random.randint(10000000, 99999999 )
                    barcod = str(barcod)
                    barcode = Barcode.query.filter_by(barcode=barcod).count()

            elif request.form['barcode']:
                barcod = request.form['barcode']
                barcode = Barcode.query.filter_by(barcode=barcod).count()
                if  barcode == 0:
                    barcod = random.randint(10000000, 99999999 )
                    barcod = str(barcod)
                    barcode = Barcode.query.filter_by(barcode=barcod).count()
                else:
                        barcod = request.form['barcode']

            barcode = Barcode.query.filter_by(barcode=barcod).count()
            if barcode == 0:
                from bar_gen import Code128
                code = str(barcod)
                full_barcode = path_barcode
                Code128(code).save(formats=['gif'],outDir=full_barcode, fnRoot=code )
                barcode_add = Barcode(cartridge=request.form['cartridge'],customer=request.form['customer'],barcode=barcod)
                session.add(barcode_add)
            order = Orders(cartridge=request.form['cartridge'],customer=request.form['customer'],tow=request.form['tow'],barcode=barcod,mark=request.form['mark'],date=request.form['date'])
            session.add(order)
            logs = Logs(user=namesd, time=date_today, message='Добавлен заказ. Штрихкод: '+barcod)
            session.add(logs)
            session.commit()
            session.flush()
            flash ('Заказ успешно добавлен')
            return redirect(url_for('orders'))

        if request.form['action'] == 'Close':
            id = request.form['id']
            user_close = request.form['user_close']
            mark = request.form['mark']
            comment = request.form['comment']
            delete = session.query(Orders).filter_by(id=id).first()
            try:
                toner = request.form['toner']
            except:
                toner = 0
            try:
                opc = request.form['opc']
            except:
                opc = 0
            try:
                pcr = request.form['pcr']
            except:
                pcr = 0
            try:
                wiper_blade = request.form['wiper_blade']
            except:
                wiper_blade = 0
            try:
                recovery_blade = request.form['recovery_blade']
            except:
                recovery_blade = 0
            try:
                develop_blade = request.form['develop_blade']
            except:
                develop_blade = 0
            try:
                doctor_blade = request.form['doctor_blade']
            except:
                doctor_blade = 0
            add = Close_orders(cartridge=delete.cartridge,customer=delete.customer,toner=toner,opc=opc,pcr=pcr,
                               wiper_blade=wiper_blade,recovery_blade=recovery_blade,develop_blade=develop_blade,
                               doctor_blade=doctor_blade,barcode=delete.barcode,mark=mark,user_close=user_close,
                               date = delete.date,date_close = date_today,comment = comment)
            session.add(add)
            session.delete(delete)
            logs = Logs(user=namesd, time=date_today, message='Закрыт заказ. Штрихкод: '+delete.barcode)
            session.add(logs)
            session.commit()
            session.flush()
            flash('Заказ успешно закрыт')
            return redirect(url_for('orders'))

    return render_template('orders.html',tows=tows, full=tmp_orders, user=user, fullnames = namesd)

@app.route('/full_order/', methods=['GET'])
@requires_auth
def full_order():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    id = request.args['id']
    user = Users.query.all()
    bar = session.query(Orders.id, Orders.barcode).filter_by(id=id).first()
    full = session.query(Orders.id, Cartridges.name, Customers.name, Tow.fullname, Orders.barcode, Orders.mark, Orders.date)\
        .filter_by(id=id)\
        .join(Cartridges, Orders.cartridge == Cartridges.id)\
        .join(Customers, Orders.customer == Customers.id)\
        .join(Tow, Orders.tow == Tow.id)

    tmp_orders = {}
    for order in full:
        if order.name not in tmp_orders:
             tmp_orders[order.name] = []
        tmp_orders[order.name].append(order)

    barcc = bar.barcode
    fuls = session.query(Close_orders.id, Cartridges.name, Customers.name, Close_orders.toner, Close_orders.opc,
                         Close_orders.pcr, Close_orders.wiper_blade, Close_orders.recovery_blade, Close_orders.develop_blade,
                         Close_orders.doctor_blade, Close_orders.barcode, Close_orders.mark,Close_orders.user_close,
                         Close_orders.date, Close_orders.date_close, Close_orders.status, Close_orders.comment)\
        .filter_by(barcode=barcc)\
        .join(Cartridges, Close_orders.cartridge == Cartridges.id)\
        .join(Customers, Close_orders.customer == Customers.id)

    tmpp_orders = {}
    for order in fuls:
        if order.barcode not in tmpp_orders:
             tmpp_orders[order.barcode] = []
        tmpp_orders[order.barcode].append(order)
		
    fulss = session.query(Archive_orders.id, Cartridges.name, Customers.name, Archive_orders.toner, Archive_orders.opc,
                          Archive_orders.pcr, Archive_orders.wiper_blade, Archive_orders.recovery_blade, Archive_orders.develop_blade,
                          Archive_orders.doctor_blade, Archive_orders.barcode, Archive_orders.mark,Archive_orders.user_close,
                          Archive_orders.date, Archive_orders.date_close, Archive_orders.status, Archive_orders.comment)\
        .filter_by(barcode=barcc)\
        .join(Cartridges, Archive_orders.cartridge == Cartridges.id)\
        .join(Customers, Archive_orders.customer == Customers.id)
    tmppp_orders = {}
    for order in fulss:
        if order.barcode not in tmppp_orders:
             tmppp_orders[order.barcode] = []
        tmppp_orders[order.barcode].append(order)

    return render_template('full_order.html', full=tmp_orders, user=user, fuls=tmpp_orders, fuls1=tmppp_orders, fullnames = namesd)

@app.route('/close_orders/', methods=['GET'])
@requires_auth
@requires_manager
def close_orders():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%Y-%m-%d")
    if request.args.get('st'):
        status = request.args.get('st')
        id = request.args.get('id')
        stmt = update(Close_orders).where(Close_orders.id == id).values(status = status)
        session.execute(stmt)
        logs = Logs(user=namesd, time=date_today, message='Изменен статус завершенного заказа №: ' + id)
        session.add(logs)
        session.commit()
        session.flush()
        flash('Статус заказа успешно изменен')
        return redirect(url_for('close_orders'))

    if request.args.get('del') == "yes":
        id = request.args.get('id')
        yes = session.query(Close_orders).filter(Close_orders.id == id).first()
        if yes.toner == 0 and yes.opc == 0 and yes.pcr == 0 and yes.wiper_blade == 0 and yes.recovery_blade == 0 and yes.develop_blade == 0 and yes.doctor_blade == 0:
            session.query(Close_orders).filter(Close_orders.id == id).delete()
            logs = Logs(user=namesd, time=date_today, message='Удален завершенный заказ №: ' + id)
            session.add(logs)
            session.commit()
            session.flush()
            flash ('Заказ был успешно удален')
            return redirect(url_for('close_orders'))

        else:
            flash ('Заказ не был удален')
            return redirect(url_for('close_orders'))

    full = session.query(Close_orders.id, Cartridges.name, Customers.name, Close_orders.toner, Close_orders.opc,
                         Close_orders.pcr, Close_orders.wiper_blade, Close_orders.recovery_blade, Close_orders.develop_blade,
                         Close_orders.doctor_blade, Close_orders.barcode, Close_orders.mark,Close_orders.user_close,
                         Close_orders.date, Close_orders.date_close, Close_orders.status)\
        .order_by(desc(Close_orders.id))\
        .join(Cartridges, Close_orders.cartridge == Cartridges.id)\
        .join(Customers, Close_orders.customer == Customers.id)

    tmp_orders = {}
    for  order in full:
        if order.name not in tmp_orders:
             tmp_orders[order.name] = []
        tmp_orders[order.name].append(order)

    return render_template('close_orders.html', full=tmp_orders, fullnames = namesd)

@app.route('/archive_orders/', methods=['GET','POST'])
@requires_auth
@requires_manager
def archive_orders():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    full = session.query(Archive_orders.id, Cartridges.name, Customers.name, Archive_orders.toner, Archive_orders.opc,
                         Archive_orders.pcr, Archive_orders.wiper_blade, Archive_orders.recovery_blade, Archive_orders.develop_blade,
                         Archive_orders.doctor_blade, Archive_orders.barcode, Archive_orders.mark, Archive_orders.user_close,
                         Archive_orders.date, Archive_orders.date_close, Archive_orders.status)\
        .order_by(desc(Archive_orders.id))\
        .join(Cartridges, Archive_orders.cartridge == Cartridges.id)\
        .join(Customers, Archive_orders.customer == Customers.id)

    tmp_orders = {}
    for  order in full:
        if order.name not in tmp_orders:
             tmp_orders[order.name] = []
        tmp_orders[order.name].append(order)
    full0 = full.count()
    cartridges = Cartridges.query.order_by(Cartridges.name).all()
    customers = Customers.query.order_by(Customers.name).all()
    users = Users.query.order_by(desc(Users.id)).all()

    if request.method == 'POST':
        if request.form['action'] == 'Sort':
            if 'toner' in request.form or 'opc' in request.form or 'pcr' in request.form or 'wiper_blade' in request.form or \
                            'recovery_blade' in request.form or 'develop_blade' in request.form or 'doctor_blade' in request.form:
                filters = []
                cartridge = request.form['cartridge']
                if cartridge != '*':
                    filters.append(Archive_orders.cartridge == cartridge)
                customer = request.form['customer']
                if customer != '*':
                    filters.append(Archive_orders.customer == customer)
                mark = request.form['mark']
                if mark != '*':
                    filters.append(Archive_orders.mark == mark)
                user = request.form['user']
                if user != '*':
                    filters.append(Archive_orders.user_close == user)
                date1 = request.form['date1']
                if date1 != '':
                    filters.append(Archive_orders.date_close >= date1)
                date2 = request.form['date2']
                if date2 != '':
                    filters.append(Archive_orders.date_close <= date2)
                try :
                    request.form['toner']
                    filters.append(Archive_orders.toner == request.form['toner'])
                except:
                    filters.append(Archive_orders.toner == 0)
                try :
                    request.form['opc']
                    filters.append(Archive_orders.opc == request.form['opc'])
                except:
                    filters.append(Archive_orders.opc == 0)
                try :
                    request.form['pcr']
                    filters.append(Archive_orders.pcr == request.form['pcr'])
                except:
                    filters.append(Archive_orders.pcr == 0)
                try :
                    request.form['wiper_blade']
                    filters.append(Archive_orders.wiper_blade == request.form['wiper_blade'])
                except:
                    filters.append(Archive_orders.wiper_blade == 0)
                try :
                    request.form['recovery_blade']
                    filters.append(Archive_orders.recovery_blade == request.form['recovery_blade'])
                except:
                    filters.append(Archive_orders.recovery_blade == 0)
                try :
                    request.form['develop_blade']
                    filters.append(Archive_orders.develop_blade == request.form['develop_blade'])
                except:
                    filters.append(Archive_orders.develop_blade == 0)
                try :
                    request.form['doctor_blade']
                    filters.append(Archive_orders.doctor_blade == request.form['doctor_blade'])
                except:
                    filters.append(Archive_orders.doctor_blade == 0)
            else:
                filters = []
                cartridge = request.form['cartridge']
                if cartridge != '*':
                    filters.append(Archive_orders.cartridge == cartridge)
                customer = request.form['customer']
                if customer != '*':
                    filters.append(Archive_orders.customer == customer)
                mark = request.form['mark']
                if mark != '*':
                    filters.append(Archive_orders.mark == mark)
                user = request.form['user']
                if user != '*':
                    filters.append(Archive_orders.user_close == user)
                date1 = request.form['date1']
                if date1 != '':
                    filters.append(Archive_orders.date_close >= date1)
                date2 = request.form['date2']
                if date2 != '':
                    filters.append(Archive_orders.date_close <= date2)
            full1 = session.query(Archive_orders.id, Cartridges.name,
                                  Customers.name, Archive_orders.toner, Archive_orders.opc,
                                  Archive_orders.pcr, Archive_orders.wiper_blade, Archive_orders.recovery_blade,
                                  Archive_orders.develop_blade,
                                  Archive_orders.doctor_blade, Archive_orders.barcode, Archive_orders.mark,
                                  Archive_orders.user_close,
                                  Archive_orders.date, Archive_orders.date_close, Archive_orders.status)\
                    .filter(*filters)\
                    .join(Cartridges, Archive_orders.cartridge == Cartridges.id)\
                    .join(Customers, Archive_orders.customer == Customers.id)
            full2 = full1.count()
            tmp_orders1 = {}
            for order in full1:
                if order.name not in tmp_orders1:
                    tmp_orders1[order.name] = []
                tmp_orders1[order.name].append(order)

            return render_template('archive_orders.html',count=full2, full=tmp_orders1, cartridges=cartridges, customers=customers,
                                   users=users, fullnames = namesd)
    return render_template('archive_orders.html', count=full0, full=tmp_orders, cartridges=cartridges, customers=customers,
                           users=users, fullnames = namesd)

@app.route('/archive_all/', methods=['GET'])
@requires_auth
@requires_manager
def archive_all():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%Y-%m-%d")
    query = session.query(Close_orders).filter(Close_orders.status == 'success').all()
    for order in query:
        cartridge = order.cartridge
        customer = order.customer
        toner = order.toner
        opc = order.opc
        pcr = order.pcr
        wiper_blade = order.wiper_blade
        recovery_blade = order.recovery_blade
        develop_blade = order.develop_blade
        doctor_blade = order.doctor_blade
        barcode = order.barcode
        mark = order.mark
        user_close = order.user_close
        date = order.date
        date_close = order.date_close
        status = order.status
        comment = order.comment
        archive = Archive_orders(cartridge=cartridge,customer=customer,toner=toner,opc=opc,pcr=pcr,wiper_blade=wiper_blade,
                                 recovery_blade=recovery_blade,develop_blade=develop_blade,doctor_blade=doctor_blade,
                                 user_close=user_close,barcode=barcode,mark=mark,date=date,date_close=date_close,status=status,
                                 comment=comment)
        session.add(archive)
        logs = Logs(user=namesd, time=date_today, message='Завершенные заказы перемещены в архив')
        session.add(logs)
        session.query(Close_orders).filter(Close_orders.id == order.id).delete()
        session.commit()
        session.flush()
        flash ('Заказы перемещены в архив')
    return redirect(url_for('close_orders'))

@app.route('/full_close_order/', methods=['GET','POST'])
@requires_auth
@requires_manager
def full_close_order():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%d.%m.%Y")
    if request.args.get('barcode'):
        barcode = request.args['barcode']
        user = Users.query.all()
        full = session.query(Close_orders, Cartridges, Customers)\
            .filter_by(barcode=barcode)\
            .join(Cartridges, Close_orders.cartridge == Cartridges.id)\
            .join(Customers, Close_orders.customer == Customers.id)

        full1 = session.query(Archive_orders, Cartridges, Customers)\
            .filter_by(barcode=barcode)\
            .join(Cartridges, Archive_orders.cartridge == Cartridges.id)\
            .join(Customers, Archive_orders.customer == Customers.id)		
			
        return render_template('full_close_order.html', user=user, full=full, full1=full1, fullnames = namesd)

    if request.form['action'] == 'Edit':
            id = request.form['id']
            user_close = request.form['user_close']
            mark = request.form['mark']
            update = session.query(Close_orders).filter_by(id=id).first()
            comment = request.form['comment']

            try:
                toner = request.form['toner']
            except:
                toner = 0
            try:
                opc = request.form['opc']
            except:
                opc = 0
            try:
                pcr = request.form['pcr']
            except:
                pcr = 0
            try:
                wiper_blade = request.form['wiper_blade']
            except:
                wiper_blade = 0
            try:
                recovery_blade = request.form['recovery_blade']
            except:
                recovery_blade = 0
            try:
                develop_blade = request.form['develop_blade']
            except:
                develop_blade = 0
            try:
                doctor_blade = request.form['doctor_blade']
            except:
                doctor_blade = 0

            session.query(Close_orders).filter(Close_orders.id == id).update({'cartridge' : update.cartridge,
                               'customer' : update.customer,'toner' : toner,'opc' : opc,'pcr' : pcr,'wiper_blade' : wiper_blade,
                               'recovery_blade' : recovery_blade,'develop_blade' : develop_blade,'doctor_blade' : doctor_blade,
                               'barcode' : update.barcode,'mark' : mark,'user_close' : user_close,'date' : update.date,
                               'date_close' : date_today, 'comment' : comment})
            logs = Logs(user=namesd, time=date_today, message='Завершенный заказ изменен. Штрихкод: '+update.barcode)
            session.add(logs)
            session.commit()
            session.flush()
            flash('Заказ успешно изменен')
            return redirect(url_for('close_orders'))

@app.route('/barcode/', methods=['GET','POST'])
@requires_auth
def barcode(rows=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%d.%m.%Y")
    full = session.query(Barcode, Cartridges,Customers).join(Cartridges, Barcode.cartridge == Cartridges.id).join(Customers, Barcode.customer == Customers.id).order_by(Barcode.id)
    cartridges = Cartridges.query.order_by(Cartridges.name).all()
    customers = Customers.query.order_by(Customers.name).all()

    if request.method == 'POST':
        if request.form['action'] == 'Find':
            if request.form['barcode']:
                barcod = request.form['barcode']
                full = session.query(Barcode, Cartridges, Customers).join(Cartridges,
                                    Barcode.cartridge == Cartridges.id).join(
                                    Customers, Barcode.customer == Customers.id).filter(Barcode.barcode.like('%'+barcod+'%')).all()
                return render_template('barcode.html', full=full, fullnames = namesd)
        else:
            flash('Штрихкод не найден')

        if request.form['action'] == 'Edit':
            barcode = request.form['barcod']
            cartridge = request.form['cartridge']
            customer = request.form['customer']
            session.query(Barcode).filter(Barcode.barcode == barcode).update({'cartridge': cartridge, 'customer': customer, 'barcode': barcode})
            session.query(Close_orders).filter(Close_orders.barcode == barcode).update({'cartridge': cartridge, 'customer': customer})
            session.query(Archive_orders).filter(Archive_orders.barcode == barcode).update({'cartridge': cartridge, 'customer': customer})
            session.query(Orders).filter(Orders.barcode == barcode).update({'cartridge': cartridge, 'customer': customer})
            logs = Logs(user=namesd, time=date_today, message='Штрихкод № ' + barcode + ' изменен')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Штрихкод был успешно изменён')
            return redirect(url_for('barcode'))

    if request.args.get('edit') == "yes":
        barcode = request.args.get('barcode')
        barcod = Barcode.query.filter_by(barcode = barcode).first()
        cartridgee = Cartridges.query.filter_by(id = barcod.cartridge).first()
        customerr = Customers.query.filter_by(id = barcod.customer).first()
        return render_template('barcode_edit.html', cartridges=cartridges, customers=customers,barcode=barcode,customerr=customerr,cartridgee=cartridgee, fullnames = namesd)

    if request.args.get('del') == "yes":
        barcode = request.args.get('barcode')
        yes = Archive_orders.query.filter_by(barcode = barcode).count()
        yess = Close_orders.query.filter_by(barcode = barcode).count()
        if yes == 0 and yess == 0:
            session.query(Barcode).filter(Barcode.barcode == barcode).delete()
            logs = Logs(user=namesd, time=date_today, message='Штрихкод № ' + barcode + ' удален')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Штрихкод был успешно удален')
            return redirect(url_for('barcode'))

        else:
            flash('Штрихкод не был удален')
            return redirect(url_for('barcode'))



    return render_template('barcode.html', full=full, cartridges=cartridges, customers=customers, fullnames = namesd)

@app.route('/statistics/', methods=['GET','POST'])
@requires_auth
@requires_boss
def statistics():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    customers = Customers.query.order_by(Customers.name).all()
    full = session.query(Archive_orders.id, Customers.id, Customers.name) \
        .join(Customers, Archive_orders.customer == Customers.id)\
        .order_by(Customers.name)

    tmp_orders1 = {}
    for order in full:
        if order.name not in tmp_orders1:
            tmp_orders1[order.name] = []
            full_work = session.query(func.min(Archive_orders.cartridge), func.min(Customers.name), Cartridges.name,
                                      func.sum(Archive_orders.toner).label('toner'),
                                      func.sum(Archive_orders.opc).label('opc'),
                                      func.sum(Archive_orders.pcr).label('pcr'),
                                      func.sum(Archive_orders.wiper_blade).label('wiper_blade'),
                                      func.sum(Archive_orders.recovery_blade).label('recovery_blade'),
                                      func.sum(Archive_orders.develop_blade).label('develop_blade'),
                                      func.sum(Archive_orders.doctor_blade).label('doctor_blade')) \
                .join(Customers, Archive_orders.customer == Customers.id) \
                .join(Cartridges, Archive_orders.cartridge == Cartridges.id) \
                .group_by(Cartridges.name) \
                .filter(Customers.name == order.name).subquery()
            full_cartridges = session.query(func.count(Barcode.barcode), Cartridges.name, func.min(full_work.c.toner),
                                            func.min(full_work.c.opc), func.min(full_work.c.pcr), func.min(full_work.c.wiper_blade),
                                            func.min(full_work.c.recovery_blade), func.min(full_work.c.develop_blade),
                                            func.min(full_work.c.doctor_blade)) \
                .join(Customers,Barcode.customer == Customers.id) \
                .join(Cartridges, Barcode.cartridge == Cartridges.id) \
                .outerjoin(full_work, Cartridges.name == full_work.c.name)\
                .group_by(Cartridges.name)\
                .filter(Customers.name == order.name).all()
            tmp_orders1[order.name].append(full_cartridges)

    if request.method == 'POST':
        if request.form['action'] == 'Sort':
            filters = []
            customer = request.form['customer']
            #if customer != '*':
                #filters.append(Archive_orders.customer == customer)
            date1 = request.form['date1']
            if date1 != '':
                filters.append(Archive_orders.date_close >= date1)
            date2 = request.form['date2']
            if date2 != '':
                filters.append(Archive_orders.date_close <= date2)
            full = session.query(Archive_orders.id, Customers.id, Customers.name) \
                .join(Customers, Archive_orders.customer == Customers.id) \
                .filter(Customers.id == customer)\
                .order_by(Customers.name)

            tmp_orders1 = {}
            for order in full:
                if order.name not in tmp_orders1:
                    tmp_orders1[order.name] = []
                    full_work = session.query(func.min(Archive_orders.cartridge), func.min(Customers.name),
                                              Cartridges.name,
                                              func.sum(Archive_orders.toner).label('toner'),
                                              func.sum(Archive_orders.opc).label('opc'),
                                              func.sum(Archive_orders.pcr).label('pcr'),
                                              func.sum(Archive_orders.wiper_blade).label('wiper_blade'),
                                              func.sum(Archive_orders.recovery_blade).label('recovery_blade'),
                                              func.sum(Archive_orders.develop_blade).label('develop_blade'),
                                              func.sum(Archive_orders.doctor_blade).label('doctor_blade')) \
                        .join(Customers, Archive_orders.customer == Customers.id) \
                        .join(Cartridges, Archive_orders.cartridge == Cartridges.id) \
                        .group_by(Cartridges.name) \
                        .filter(Customers.name == order.name,*filters).subquery()
                    full_cartridges = session.query(func.count(Barcode.barcode), Cartridges.name,
                                                    func.min(full_work.c.toner),
                                                    func.min(full_work.c.opc), func.min(full_work.c.pcr),
                                                    func.min(full_work.c.wiper_blade),
                                                    func.min(full_work.c.recovery_blade),
                                                    func.min(full_work.c.develop_blade),
                                                    func.min(full_work.c.doctor_blade)) \
                        .join(Customers, Barcode.customer == Customers.id) \
                        .join(Cartridges, Barcode.cartridge == Cartridges.id) \
                        .outerjoin(full_work, Cartridges.name == full_work.c.name) \
                        .group_by(Cartridges.name) \
                        .filter(Customers.name == order.name).all()
                    tmp_orders1[order.name].append(full_cartridges)
        return render_template('statistics.html', full1=tmp_orders1, customers=customers, fullnames=namesd)
    return render_template('statistics.html', full1=tmp_orders1, customers=customers, fullnames = namesd)

@app.route('/settings/')
@requires_auth
@requires_admin
def settings():
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    return render_template('settings.html', fullnames = namesd)

@app.route('/cartridges/', methods=['GET','POST'])
@requires_auth
def cartridges(rows=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%d.%m.%Y")
    if request.args.get('del') == "yes":
        id = request.args.get('id')
        yes = Archive_orders.query.filter_by(cartridge=id).count()
        yess = Close_orders.query.filter_by(cartridge=id).count()
        cart = session.query(Cartridges).filter(Cartridges.id == id).one()
        if yes == 0 and yess == 0:
            session.query(Cartridges).filter(Cartridges.id == id).delete()
            logs = Logs(user=namesd, time=date_today, message='Картридж ' + cart.name + ' удален')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Картридж успешно удален')
            return redirect(url_for('cartridges'))

        else:
            flash('Картридж не удален')
            return redirect(url_for('cartridges'))

    if request.method == 'POST':
        if request.form['action'] == 'Add':
            return render_template('cartridge_add.html', fullnames = namesd)

        if request.form['action'] == 'Cancel':
            return redirect(url_for('cartridges'))

        if request.form['action'] == 'Find':
            if request.form['name']:
                name = request.form['name']
                cartridges = session.query(Cartridges).filter(Cartridges.name.like('%'+name+'%')).all()
                return render_template('cartridges.html', rows=cartridges, fullnames = namesd)
        else:
            flash('Картридж не найден')

        if request.form['action'] == 'Edit':
            id = request.form['id']
            name = request.form['name']
            printer = request.form['printer']
            try:
                toner = request.form['toner']
            except:
                toner = 0
            try:
                opc = request.form['opc']
            except:
                opc = 0
            try:
                pcr = request.form['pcr']
            except:
                pcr = 0
            try:
                wiper_blade = request.form['wiper_blade']
            except:
                wiper_blade = 0
            try:
                recovery_blade = request.form['recovery_blade']
            except:
                recovery_blade = 0
            try:
                develop_blade = request.form['develop_blade']
            except:
                develop_blade = 0
            try:
                doctor_blade = request.form['doctor_blade']
            except:
                doctor_blade = 0
            try:
                printer = request.form['printer']
            except:
                printer = ""
            session.query(Cartridges).filter(Cartridges.id == id).update(
                {'name': name, 'toner': toner, 'opc': opc, 'pcr': pcr, 'wiper_blade': wiper_blade, 'recovery_blade': recovery_blade,
                 'develop_blade': develop_blade, 'doctor_blade': doctor_blade, 'printers': printer})
            logs = Logs(user=namesd, time=date_today, message='Картридж ' + name + ' изменен')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Картридж успешно изменён')
            return redirect(url_for('cartridges'))

        if request.form['action'] == 'Adds':
            name = request.form['name']
            try:
                toner = request.form['toner']
            except:
                toner = 0
            try:
                opc = request.form['opc']
            except:
                opc = 0
            try:
                pcr = request.form['pcr']
            except:
                pcr = 0
            try:
                wiper_blade = request.form['wiper_blade']
            except:
                wiper_blade = 0
            try:
                recovery_blade = request.form['recovery_blade']
            except:
                recovery_blade = 0
            try:
                develop_blade = request.form['develop_blade']
            except:
                develop_blade = 0
            try:
                doctor_blade = request.form['doctor_blade']
            except:
                doctor_blade = 0
            try:
                printer = request.form['printer']
            except:
                printer = ""
            cartridge = Cartridges(name=name,toner=toner,opc=opc,pcr=pcr,wiper_blade=wiper_blade,recovery_blade=recovery_blade,
                                   develop_blade=develop_blade,doctor_blade=doctor_blade,printers=printer)
            session.add(cartridge)
            logs = Logs(user=namesd, time=date_today, message='Картридж ' + name + ' добавлен')
            session.add(logs)
            session.commit()
            session.flush()
            flash ('Картридж успешно добавлен')
            return redirect(url_for('cartridges'))

    cartridges = Cartridges.query.order_by('name').all()
    return render_template('cartridges.html',rows=cartridges, fullnames = namesd)

@app.route('/customers/', methods=['GET','POST'])
@requires_auth
def customers(rows=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    date = datetime.date.today()
    date_today = date.strftime("%d.%m.%Y")
    if request.args.get('del') == "yes":
        id = request.args.get('id')
        yes = Archive_orders.query.filter_by(customer=id).count()
        yess = Close_orders.query.filter_by(customer=id).count()
        cust = session.query(Customers).filter(Customers.id == id).one()
        if yes == 0 and yess == 0:
            session.query(Customers).filter(Customers.id == id).delete()
            logs = Logs(user=namesd, time=date_today, message='Клиент ' + cust.name + ' удален')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Клиент успешно удален')
            return redirect(url_for('customers'))
        else:
            flash('Клиент не удален')
            return redirect(url_for('customers'))

    if request.method == 'POST':
        if request.form['action'] == 'Add':
            return render_template('customer_add.html', fullnames = namesd)
        if request.form['action'] == 'Full':
            return render_template('full_customers.html', fullnames = namesd)
        if request.form['action'] == 'Cancel':
            return redirect(url_for('customers'))

        if request.form['action'] == 'Find':
            if request.form['name']:
                name = request.form['name']
                customers = session.query(Customers).filter(Customers.name.like('%' + name + '%')).all()
                customerss = session.query(Customers).filter(Customers.inn.like('%' + name + '%')).all()
                return render_template('customers.html', rows=customers, rowss=customerss, fullnames = namesd)
        else:
            flash('Картридж не найден')

        if request.form['action'] == 'Edit':
            id = request.form['id']
            name = request.form['name']
            inn = request.form['inn']
            try:
                inn = request.form['inn']
            except:
                inn = ""
            session.query(Customers).filter(Customers.id == id).update(
                {'name': name, 'inn': inn})
            logs = Logs(user=namesd, time=date_today, message='Клиент ' + name + ' изменен')
            session.add(logs)
            session.commit()
            session.flush()
            flash('Клиент успешно изменён')
            return redirect(url_for('customers'))

        if request.form['action'] == 'Adds':
            name = request.form['name']
            try:
                inn = request.form['inn']
            except:
                inn = ""
            customer = Customers(name=name,inn=inn)
            session.add(customer)
            logs = Logs(user=namesd, time=date_today, message='Клиент ' + name + ' добавлен')
            session.add(logs)
            session.commit()
            session.flush()
            flash ('Клиент успешно добавлен')
            return redirect(url_for('customers'))
    customers = Customers.query.order_by('name').all()
    return render_template('customers.html',rows=customers, fullnames = namesd)

@app.route('/tow/', methods=['GET','POST'])
@requires_auth
def tow(rows=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            return render_template('tow_add.html', fullnames = namesd)
        if request.form['action'] == 'Full':
            return render_template('full_tow.html', fullnames = namesd)
        if request.form['action'] == 'Cancel':
            return redirect(url_for('tow'))
        if request.form['action'] == 'Adds':
            category = Category(name=request.form['name'])
            session.add(category)
            flash ('Категория успешно добалена')
            return redirect(url_for('tow'))
    tow = Tow.query.all()
    return render_template('tow.html',rows=tow, fullnames = namesd)

@app.route('/logs/')
@requires_auth
@requires_boss
def logs(logs=None):
    auth = request.authorization
    user1 = session.query(Users).filter_by(name=auth.username).first()
    namesd = user1.fullname
    logs = session.query(Logs).all()
    return render_template('logs.html', logs=logs, fullnames = namesd)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug='True')
