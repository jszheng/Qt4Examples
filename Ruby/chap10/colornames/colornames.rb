require 'Qt'

class ColorNamesDialog < Qt::Dialog
  slots 'reApplyFilter()'

  def initialize(parent=nil)
    super(parent)

    @source_model = Qt::StringListModel.new(Qt::Color.colorNames())

    @proxy_model = Qt::SortFilterProxyModel.new(self)
    @proxy_model.setSourceModel(@source_model)
    @proxy_model.setFilterKeyColumn(0)

    @list_view = Qt::ListView.new()
    @list_view.setModel(@proxy_model)
    @list_view.setEditTriggers(Qt::AbstractItemView::NoEditTriggers)

    @filter_label = Qt::Label.new('&Filter:')
    @filter_line_edit = Qt::LineEdit.new()
    @filter_label.buddy = @filter_line_edit

    @syntax_label = Qt::Label.new('&Pattern syntax:')
    @combo = Qt::ComboBox.new()
    @combo.addItem('Regular expression')
    @combo.addItem('Wildcard')
    @combo.addItem('Fixed String')
    @syntax_label.buddy = @combo

    @grid_layout = Qt::GridLayout.new()
    @grid_layout.addWidget(@list_view, 0, 0, 1, 2)

    @grid_layout.addWidget(@filter_label,     1, 0)
    @grid_layout.addWidget(@filter_line_edit, 1, 1)

    @grid_layout.addWidget(@syntax_label, 2, 0)
    @grid_layout.addWidget(@combo,        2, 1)

    setLayout(@grid_layout)
    setWindowTitle('Color Names')

    connect(@filter_line_edit, SIGNAL('textChanged(const QString&)'),
            self, SLOT('reApplyFilter()'))
    connect(@combo, SIGNAL('currentIndexChanged(int)'),
            self, SLOT('reApplyFilter()'))
  end

  def reApplyFilter()
    regexp_table = [
        Qt::RegExp::RegExp,
        Qt::RegExp::Wildcard,
        Qt::RegExp::FixedString
    ]
    index = @combo.currentIndex()
    syntax = regexp_table[index]
    text = @filter_line_edit.text
    regexp = Qt::RegExp.new(text, Qt::CaseInsensitive, syntax)
    @proxy_model.setFilterRegExp(regexp)
  end

end