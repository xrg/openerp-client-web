// Calendar i18n
// Language: zh-cn (Chinese, China)
// Encoding: gbk
// Author: muziq, <muziq@sina.com>, nEO<gentoo.cn@gmail.com>
// Distributed under the same terms as the calendar itself.

// full day names
Calendar._DN = new Array
("������",
 "����һ",
 "���ڶ�",
 "������",
 "������",
 "������",
 "������",
 "������");

// short day names
Calendar._SDN = new Array
("��",
 "һ",
 "��",
 "��",
 "��",
 "��",
 "��",
 "��");

// First day of the week. "0" means display Sunday first.
Calendar._FD = 0;

// full month names
Calendar._MN = new Array
("һ��",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "ʮ��",
 "ʮһ��",
 "ʮ����");

// short month names
Calendar._SMN = new Array
("һ��",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "����",
 "ʮ��",
 "ʮһ��",
 "ʮ����");

// tooltips
Calendar._TT = {};
Calendar._TT["INFO"] = "����";

Calendar._TT["ABOUT"] =
"DHTML Date/Time Selector\n" +
"(c) dynarch.com 2002-2005 / Author: Mihai Bazon\n" + // don't translate this this ;-)
"For latest version visit: http://www.dynarch.com/projects/calendar/\n" +
"Distributed under GNU LGPL.  See http://gnu.org/licenses/lgpl.html for details." +
"\n\n" +
"ѡ������:\n" +
"- ��� \xab, \xbb ��ťѡ�����\n" +
"- ��� " + String.fromCharCode(0x2039) + ", " + String.fromCharCode(0x203a) + " ��ťѡ���·�\n" +
"- �������ϰ�ť�ɴӲ˵��п���ѡ����ݻ��·�";
Calendar._TT["ABOUT_TIME"] = "\n\n" +
"ѡ��ʱ��:\n" +
"- ���Сʱ����ӿ�ʹ����ֵ��һ\n" +
"- ��סShift�����Сʱ����ӿ�ʹ����ֵ��һ\n" +
"- ����϶����ɽ��п���ѡ��";

Calendar._TT["PREV_YEAR"] = "��һ�� (��ס���˵�)";
Calendar._TT["PREV_MONTH"] = "��һ�� (��ס���˵�)";
Calendar._TT["GO_TODAY"] = "ת������";
Calendar._TT["NEXT_MONTH"] = "��һ�� (��ס���˵�)";
Calendar._TT["NEXT_YEAR"] = "��һ�� (��ס���˵�)";
Calendar._TT["SEL_DATE"] = "ѡ������";
Calendar._TT["DRAG_TO_MOVE"] = "�϶�";
Calendar._TT["PART_TODAY"] = " (����)";

// the following is to inform that "%s" is to be the first day of week
// %s will be replaced with the day name.
Calendar._TT["DAY_FIRST"] = "�������ʾ%s";

// This may be locale-dependent.  It specifies the week-end days, as an array
// of comma-separated numbers.  The numbers are from 0 to 6: 0 means Sunday, 1
// means Monday, etc.
Calendar._TT["WEEKEND"] = "0,6";

Calendar._TT["CLOSE"] = "�ر�";
Calendar._TT["TODAY"] = "����";
Calendar._TT["TIME_PART"] = "(Shift-)��������϶��ı�ֵ";

// date formats
Calendar._TT["DEF_DATE_FORMAT"] = "%Y-%m-%d";
Calendar._TT["TT_DATE_FORMAT"] = "%A, %b %e��";

Calendar._TT["WK"] = "��";
Calendar._TT["TIME"] = "ʱ��:";