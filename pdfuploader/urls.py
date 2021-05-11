from django.conf.urls import url
from .views import RedisView
from .views import PdfView
from .views import pdfCheck

from .views import ChequeBounce
from .views import Top5Credit
from .views import Top5Debit
from .views import balances
from .views import Loan
from .views import FundRecieved
from .views import FundRemittances
from .views import AnalysisSheets
from .views import Frequent_Cr
from .views import Frequent_db
from .views import AverageMonthly
from .views import OpeningBal
from .views import Penalty
from .views import Credit
from .views import dividend
from .views import HighValue
from .views import CreditAnalysis
from .views import DebitAnalysis
from .views import FinancialAnalysis
from .views import InternalTxn
from .views import InterestAnalysis
from .views import LoanAnalysis
from .views import AverageQAnalysis
from .views import ChartsFrequent
from .views import StatementCharts
from .views import NonRev
from .views import SalaryAnalysis
from django.urls import path
from pdfuploader import views

urlpatterns = [
	url(r'^redisview/' , RedisView.as_view(), name='redisview'),
    url(r'^upload/', PdfView.as_view(), name='pdf_upload'),
    url(r'^pdfcheck/', pdfCheck.as_view(), name='checker'),
    
    url(r'^cheque_bounce/' , ChequeBounce.as_view(), name='cheque_bounce'),
    url(r'^top5credit/' , Top5Credit.as_view(), name='top5credit'),
    url(r'^top5debit/' , Top5Debit.as_view(), name='top5debit'),
    url(r'^balances/' , balances.as_view(), name='balances'),
    url(r'^loan/' , Loan.as_view(), name='loan'),
    url(r'^fund_rec/' , FundRecieved.as_view(), name='fund_rec'),
    url(r'^FundRem/' , FundRemittances.as_view(), name='FundRem'),
    url(r'^analysisSheets/' , AnalysisSheets.as_view(), name='analysisSheets'),
    url(r'^frequentcr/' , Frequent_Cr.as_view(), name='frequentcr'),
    url(r'^frequentdb/' , Frequent_db.as_view(), name='frequentdb'),
    url(r'^averagemonthly/' , AverageMonthly.as_view(), name='averagemonthly'),
    url(r'^opening_bal/' , OpeningBal.as_view(), name='opening_bal'),
    url(r'^penalty/' , Penalty.as_view(), name='penalty'),
    url(r'^credit/' , Credit.as_view(), name='credit'),
    url(r'^dividend/' , dividend.as_view(), name='dividend'),
    url(r'^highvalue/' , HighValue.as_view(), name='highvalue'),
    url(r'^credit_analysis/' , CreditAnalysis.as_view(), name='credit_analysis'),
    url(r'^debit_analysis/' , DebitAnalysis.as_view(), name='debit_analysis'),
    url(r'^finance_analysis/' , FinancialAnalysis.as_view(), name='finance_analysis'),
    url(r'^internal_txn/' , InternalTxn.as_view(), name='internal_txn'),
    url(r'^interest_analysis/' , InterestAnalysis.as_view(), name='interest_analysis'),
    url(r'^average_Quaterly_analysis/' , AverageQAnalysis.as_view(), name='average_Quaterly_analysis'),
    url(r'^loan_analysis/' , LoanAnalysis.as_view(), name='loan_analysis'),
    url(r'^chartsfrequent/' , ChartsFrequent.as_view(), name='chartsfrequent'),
    url(r'^statement_charts/' , StatementCharts.as_view(), name='statement_charts'),
    url(r'^Non_rev/' , NonRev.as_view(), name='Non_rev'),
    url(r'^salary_analysis/' , SalaryAnalysis.as_view(), name='salary_analysis'),
    #path('cheque_bounce/', views.cheque_bounce, name='cheque_bounce'),
    #path('top5credit/', views.top5Credit, name='credit'),
    #path('top5debit/', views.top5Debit, name='debit')
]
