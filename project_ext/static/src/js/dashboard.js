odoo.define("project_ext.dashboard", function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var web_client = require('web.web_client');
    var _t = core._t;
    var framework = require('web.framework');
    var session = require('web.session');
    var DashBoard = AbstractAction.extend({
        contentTemplate: 'Dashboard',
        events: {
            'change #project_task_selection': 'onclick_project_task_selection',
            'change #assignee_selection': 'onchange_assignee_selection',
        },
        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['ProjectTaskLineGraph'];
        },
        willStart: function() {
            var self = this;
            return $.when(this._super()).then(function() {
                return;
            });
        },
        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards();
                self.render_graphs();
                self.$el.parent().addClass('oe_background_grey');
            });
        },
        render_dashboards: function() {
            var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}));
            });
        },
        render_graphs: function(){
            var self = this;
            self.render_project_line_graph();
        },
        render_project_line_graph:function(){
            var self = this;
            rpc.query({
                model: "project.project",
                method: "get_projects",
                args: [1, 'all'],
            }).then(function (result) {
                var tasks = result.tasks;
                var assignees = result.assignees;
                self.update_task_table(tasks);
                self.update_assignee_selection(assignees);
                self.render_chart(result.projects, result.count);
            });
        },
        update_task_table: function(tasks) {
            var $table = $('#category_table');
            $table.find('tr:gt(0)').remove(); // Clear existing rows except the header
            tasks.forEach(function(task) {
                var $row = $('<tr>');
                $row.append($('<td>').text(task.name));
                $row.append($('<td>').text(task.assignee));
                $row.append($('<td>').text(task.create_date));
                $row.append($('<td>').text(task.due_date));
                $row.append($('<td>').text(task.project));
                $table.append($row);
            });
        },
        update_assignee_selection: function(assignees) {
            var $assigneeSelect = $('#assignee_selection');
            $assigneeSelect.empty(); // Clear existing options
            $assigneeSelect.append($('<option>').attr('value', 'all').text('All')); // Add default option
            assignees.forEach(function(assignee) {
                $assigneeSelect.append($('<option>').attr('value', assignee.name).attr('id', assignee.id).text(assignee.name));
            });
        },
        render_chart: function(projects, count) {
            var ctx = this.$("#canvaspie");
            var j = 0;
            $('#pro_info td').remove();
            Object.entries(count).forEach(([key, value]) => {
                $('#pro_info').append('<tr><td>'+projects[j]+'</td><td>'+value+'</td></tr>');
                j++;
            });
            $('#pro_info').hide();
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: projects, // x axis
                    datasets: [{
                        label: 'Task Count', // Name the series
                        data: count, // Specify the data values array
                        backgroundColor: [
                            "#003f5c", "#2f4b7c", "#f95d6a", "#665191", "#d45087",
                            "#ff7c43", "#ffa600", "#a05195", "#6d5c16", "#CCCCFF"
                        ],
                        borderColor: [
                            "#003f5c", "#2f4b7c", "#f95d6a", "#665191", "#d45087",
                            "#ff7c43", "#ffa600", "#a05195", "#6d5c16", "#CCCCFF"
                        ],
                        barPercentage: 0.5,
                        barThickness: 6,
                        maxBarThickness: 8,
                        minBarLength: 0,
                        borderWidth: 1, // Specify bar border width
                        type: 'line', // Set this data to a line chart
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        },
                    },
                    responsive: true, // Instruct chart js to respond nicely.
                    maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                }
            });
        },
        onclick_project_task_selection: function(events) {
            var option = $(events.target).val();
            var self = this;
            rpc.query({
                model: "project.project",
                method: "get_projects",
                args: [1, option],
            }).then(function (result) {
                var tasks = result.tasks;
                const assignees = result.assignees;
                self.update_assignee_selection(assignees);
                self.update_task_table(tasks);
                self.render_chart(result.projects, result.count);
            });
        },
        onchange_assignee_selection: function(events) {
            var selectedAssignee = $(events.target).val();
            var $rows = $('#category_table tr:gt(0)'); // Get all rows except the header
            $rows.show(); // Show all rows initially
            if (selectedAssignee !== 'all') {
                $rows.filter(function() {
                    return $(this).find('td:eq(1)').text() !== selectedAssignee;
                }).hide(); // Hide rows that do not match the selected assignee
            }
        },
    });
    core.action_registry.add('project_dashboard_tag', DashBoard);
    return DashBoard;
});