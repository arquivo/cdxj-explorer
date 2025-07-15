
        # These are extra filters that were cut out from the main program for the sake of simplicity.
        # It's only the menu layout, the actual filtering wasn't implemented.

        menu_row4 = QHBoxLayout()

        filter_layout = QHBoxLayout()

        filter_col1_layout = QVBoxLayout()
        filter_col2_layout = QVBoxLayout()
        filter_col3_layout = QVBoxLayout()
        filter_col4_layout = QVBoxLayout()
        
        filter_mime = QHBoxLayout()
        filter_mime_label = QLabel("mime:")
        self.filter_mime_input = QLineEdit()
        filter_mime.addWidget(filter_mime_label)
        filter_mime.addWidget(self.filter_mime_input)
        filter_col1_layout.addLayout(filter_mime)

        filter_status = QHBoxLayout()
        filter_status_label = QLabel("status:")
        self.filter_status_input = QLineEdit()
        filter_status.addWidget(filter_status_label)
        filter_status.addWidget(self.filter_status_input)
        filter_col1_layout.addLayout(filter_status)

        filter_layout.addLayout(filter_col1_layout)

        filter_digest = QHBoxLayout()
        filter_digest_label = QLabel("digest:")
        self.filter_digest_input = QLineEdit()
        filter_digest.addWidget(filter_digest_label)
        filter_digest.addWidget(self.filter_digest_input)
        filter_col2_layout.addLayout(filter_digest)

        filter_length = QHBoxLayout()
        filter_length_label = QLabel("length:")
        self.filter_length_input = QLineEdit()
        filter_length.addWidget(filter_length_label)
        filter_length.addWidget(self.filter_length_input)
        filter_col2_layout.addLayout(filter_length)

        filter_layout.addLayout(filter_col2_layout)

        filter_offset = QHBoxLayout()
        filter_offset_label = QLabel("offset:")
        self.filter_offset_input = QLineEdit()
        filter_offset.addWidget(filter_offset_label)
        filter_offset.addWidget(self.filter_offset_input)
        filter_col3_layout.addLayout(filter_offset)

        filter_filename = QHBoxLayout()
        filter_filename_label = QLabel("filename:")
        self.filter_filename_input = QLineEdit()
        filter_filename.addWidget(filter_filename_label)
        filter_filename.addWidget(self.filter_filename_input)
        filter_col3_layout.addLayout(filter_filename)

        filter_layout.addLayout(filter_col3_layout)

        filter_collection = QHBoxLayout()
        filter_collection_label = QLabel("collection:")
        self.filter_collection_input = QLineEdit()
        filter_collection.addWidget(filter_collection_label)
        filter_collection.addWidget(self.filter_collection_input)
        filter_col4_layout.addLayout(filter_collection)

        filter_custom = QHBoxLayout()
        filter_custom_label = QLabel("custom:")
        self.filter_custom_input = QLineEdit()
        filter_custom.addWidget(filter_custom_label)
        filter_custom.addWidget(self.filter_custom_input)
        filter_col4_layout.addLayout(filter_custom)

        filter_layout.addLayout(filter_col4_layout)
        collapsible = QCollapsibleBox(filter_layout, True)
        collapsible.setLabel("Metadata filter:")
        menu_row4.addWidget(collapsible)

        menu.addLayout(menu_row4)
